#!/usr/bin/env python3
"""8610 beam witness-hunter: min monotone circuit in lattice P(16)x P(24).
state (E,J); AND -> (E&E', J&J'), OR -> (E|E', J|J'); target (0xFFFF,0).
Beam keeps top-K states by (cost, -|E|, +|J|). Not a lower bound - witness finder."""
import json, re
d = json.load(open('/tmp/probe.json'))
st = d['gap']['statement']
IN = [int(x) for x in re.findall(r'\((\d+) : ℕ\)', re.search(r'x6 ↑x9 = \[(.*?)\]\.getD', st, re.S).group(1))]
S = [(m & 0xFFFF, (m >> 16) & 0xFFFFFF) for m in IN]
CAP, K = 21, 4000
costs = {}
par = {}
def better(E, J, c, p):
    b = costs.get((E, J))
    if b is not None and b <= c: return
    costs[(E, J)] = c
    par[(E, J)] = p
for i, (E, J) in enumerate(S):
    better(E, J, 0, ('in', i))
cur = sorted(set(S), key=lambda k: (costs[k], -bin(k[0]).count('1'), bin(k[1]).count('1')))
found = None
for rnd in range(1, 25):
    nxt = {}
    n = len(cur)
    for i in range(n):
        Ei, Ji = cur[i]
        ci = costs[(Ei, Ji)]
        for j in range(i, n):
            Ej, Jj = cur[j]
            cj = costs[(Ej, Jj)]
            cc = ci + cj + 1
            if cc > CAP: continue
            a = (Ei & Ej, Ji & Jj)
            o = (Ei | Ej, Ji | Jj)
            for stt, op in ((a, 'and'), (o, 'or')):
                if cc < min(costs.get(stt, 10**9), nxt.get(stt, 10**9)):
                    nxt[stt] = cc
                    par[stt] = (op, (Ei, Ji), (Ej, Jj))
    for (E, J), cc in nxt.items():
        if (E, J) not in costs or cc < costs[(E, J)]:
            costs[(E, J)] = cc
    allst = list(costs)
    allst.sort(key=lambda k: (costs[k], -bin(k[0]).count('1'), bin(k[1]).count('1')))
    cur = allst[:K]
    for k in list(costs):
        if costs[k] > CAP: del costs[k]
    print('round', rnd, 'live', len(allst), 'best target', costs.get((0xFFFF, 0)), flush=True)
    t = costs.get((0xFFFF, 0))
    if t is not None and t <= CAP:
        found = t
        break
if found:
    print('WITNESS TREE COST', found)
    def rec(k):
        p = par[k]
        if p[0] == 'in': return [('in', p[1])]
        return rec(p[1]) + rec(p[2]) + [(p[0], k)]
    tree = rec((0xFFFF, 0))
    json.dump([[g[0], list(g[1])] if g[0] != 'in' else ['in', g[1]] for g in tree], open('/tmp/maskdp_tree.json', 'w'))
    print('tree saved /tmp/maskdp_tree.json')
else:
    print('no witness within beam (tree-cost sense) up to 21')
