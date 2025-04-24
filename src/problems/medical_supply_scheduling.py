import numpy as np

class MedicalSupplyScheduling:
    def __init__(self, m, n, K, K1, K2, wk, ro, rs, rm, rv, aik, ajk, cijk, cjjk, coij, csij, cmij, cvij, bjk, no_i, ns_i, nm_i, nv_i, no_j, ns_j, nm_j, nv_j, C, S):
        self.m = m      # civilian medical services
        self.n = n      # military medical services
        self.K = K      # total supplies
        self.K1 = K1    # non-fixed supplies
        self.K2 = K2    # fixed supplies
        self.wk = wk    # importance weights
        self.ro = ro    # supply per normal resident
        self.rs = rs    # supply per suspected case
        self.rm = rm    # supply per mild case
        self.rv = rv    # supply per severe case
        self.aik = aik  # civilian supply available
        self.ajk = ajk  # military supply available
        self.cijk = cijk
        self.cjjk = cjjk
        self.coij = coij
        self.csij = csij
        self.cmij = cmij
        self.cvij = cvij
        self.bjk = bjk
        self.no_i = no_i
        self.ns_i = ns_i
        self.nm_i = nm_i
        self.nv_i = nv_i
        self.no_j = no_j
        self.ns_j = ns_j
        self.nm_j = nm_j
        self.nv_j = nv_j
        self.C = C
        self.S = S

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['m'], data['n'], data['K'], data['K1'], data['K2'], data['wk'], data['ro'], data['rs'],
            data['rm'], data['rv'], data['aik'], data['ajk'], data['cijk'], data['cjjk'], data['coij'],
            data['csij'], data['cmij'], data['cvij'], data['bjk'], data['no_i'], data['ns_i'], data['nm_i'],
            data['nv_i'], data['no_j'], data['ns_j'], data['nm_j'], data['nv_j'], data['C'], data['S']
        )

    def supply_satisfaction_rate(self, xijk, xjjk, yo, ys, ym, yv):
        m, n, K, K1 = self.m, self.n, self.K, self.K1
        total_satisfaction = 0.0
        total_weight = 0.0

        # Civilian medical services
        for i in range(m):
            # Final numbers to be served
            no_final = self.no_i[i] - sum(yo[i][j] for j in range(n))
            ns_final = self.ns_i[i] - sum(ys[i][j] for j in range(n))
            nm_final = self.nm_i[i] - sum(ym[i][j] for j in range(n))
            nv_final = self.nv_i[i] - sum(yv[i][j] for j in range(n))
            for k in range(K):
                rik = no_final * self.ro[k] + ns_final * self.rs[k] + nm_final * self.rm[k] + nv_final * self.rv[k]
                if k < K1:
                    aik_final = self.aik[i][k] + sum(xijk[i][j][k] for j in range(n))
                else:
                    aik_final = self.aik[i][k]
                sat = min(aik_final / rik, 1) if rik > 0 else 1
                total_satisfaction += self.wk[k] * sat
                total_weight += self.wk[k]

        # Open military medical services
        for j in range(n):
            no_final = sum(yo[i][j] for i in range(m))
            ns_final = sum(ys[i][j] for i in range(m))
            nm_final = sum(ym[i][j] for i in range(m))
            nv_final = sum(yv[i][j] for i in range(m))
            for k in range(K):
                rjk = no_final * self.ro[k] + ns_final * self.rs[k] + nm_final * self.rm[k] + nv_final * self.rv[k]
                if k < K1:
                    ajk_final = self.ajk[j][k] + sum(xijk[i][j][k] for i in range(m)) + sum(xjjk[j][jp][k] for jp in range(n))
                else:
                    ajk_final = self.ajk[j][k]
                sat = min(ajk_final / rjk, 1) if rjk > 0 else 1
                total_satisfaction += self.wk[k] * sat
                total_weight += self.wk[k]

        # Normalize by total weight (as in the paper)
        return total_satisfaction / total_weight if total_weight > 0 else 0.0

    def scheduling_cost(self, xijk, xjjk, yo, ys, ym, yv):
        cost = 0.0
        # 1. Supply delivery costs (military to civilian)
        for i in range(self.m):
            for j in range(self.n):
                for k in range(self.K1):
                    cost += self.cijk[i][j][k] * xijk[i][j][k]
        # 2. Supply delivery costs (closed to open military)
        for j in range(self.n):
            for jp in range(self.n):
                for k in range(self.K1):
                    cost += self.cjjk[j][jp][k] * xjjk[j][jp][k]
        # 3. Patient transfer costs
        for i in range(self.m):
            for j in range(self.n):
                cost += self.coij[i][j] * yo[i][j]
                cost += self.csij[i][j] * ys[i][j]
                cost += self.cmij[i][j] * ym[i][j]
                cost += self.cvij[i][j] * yv[i][j]
        return cost

    def evaluate(self, xijk, xjjk, yo, ys, ym, yv):
        # Objective 1: maximize supply satisfaction rate
        satisfaction = self.supply_satisfaction_rate(xijk, xjjk, yo, ys, ym, yv)
        # Objective 2: minimize scheduling cost (scaled as in the paper)
        cost = self.scheduling_cost(xijk, xjjk, yo, ys, ym, yv)
        cost_obj = 1 - min(cost, self.C) / (2 * self.C)
        return satisfaction, cost_obj