# Note 2: the AND/OR table search on L-meta-8610 — structure, a saturation experiment, and a question

*(found while holding the step; ahfkdy7)*

## The instance

L-meta-8610 asks for at most 21 gates of fan-in two, each `&&&` (AND) or `|||` (OR), over the
11 vertex-membership columns of the 40-row table below, with some wire reading exactly the 16
edge-rows and three distinct AND-gates reading some non-edge row. Equivalently, over graph `G`:

    edges (rows 0..15):  0:9 0:10 1:4 1:8 2:5 2:10 3:6 3:7 4:8 4:10 5:8 5:9 6:7 6:10 7:9 8:9
    rows 16..39:         the 24 maximal independent sets of G
    columns (the given masks): 2147418115, 663661903884, 34144976944, 728266375360, 21653750532,
    103293914128, 26322415680, 344922804352, 414195942664, 581968119809, 1065151898146

G has 11 vertices, 16 edges, degrees 2,2,2,2,3,3,3,3,4,4,4 and is C4-free: no pair of vertices
has two common neighbours (checked by enumeration).

## The structure: a lattice of set pairs

Every wire of every circuit is a 40-bit mask; split it as `(E, J)` with `E` the edge-rows (16
bits) and `J` the maximal-independent rows (24 bits). The gate operations act componentwise:

    AND: (E1, J1) &&& (E2, J2) = (E1 & E2, J1 & J2)
    OR:  (E1, J1) ||| (E2, J2) = (E1 | E2, J1 | J2)

So the step asks for a monotone `{AND,OR}`-circuit of at most 21 gates computing the target
`(E(G), empty)` in the product lattice `P(E(G)) x P(MIS(G))`, starting from the 11 vertex
columns `(edges through v, MISes containing v)`, with three distinct AND-type gates of nonzero
`J` (the non-degeneracy clause). This reformulation is the whole content of the step - a clean
object: the second component is *pure junk* that must be driven to zero.

## Why the easy packings miss

* **Packing (the 8031 style).** An edge-pair AND is a singleton `({k}, empty)`: 16 singletons
  plus a 15-OR tree is 31 gates > 21. So the L_meta_8031_719-style packing cannot witness this
  step; a witness would need a fundamentally different shape.
* **The C4 trick fails here.** For the 4-cycle, `AND(OR(x0,x2), OR(x1,x3))` realizes the edge
  function on its table with 3 gates, because the two diagonal independent sets are split by
  the two ORs. More generally, for `A subset V` the column `OR(A)` has junk = the maximal
  independent sets hitting `A`: with `A` a vertex cover that is 23 of the 24 rows, and an AND
  of two such columns still leaves 22 junk rows (two covers `A, B` kill an MIS only when it
  misses both, and with `24` maximal sets versus `alpha(G)`-sized independent holders, no
  constant number of `AND(OR(A), OR(B))` layers clears them all within the budget). (On this
  instance `alpha(G) = 4`, vertex covers have at least 7 vertices, the maximal independent sets
  are the 24 listed rows of sizes 3 and 4; the two-OR split above leaves 22 of 24 rows junk,
  and a three-layer input-OR construction already costs more than the 21-gate budget.)

## Saturation experiment (no 21-gate TREE witness)

A bottom-up exhaustive search over the lattice with Pareto dominance (at equal `E`, smaller `J`
at no greater cost dominates, since both operations are componentwise monotone) reaches a
fixpoint: every `(E, J)` expressible by a tree (unshared) circuit of cost <= 21 is among
**2,173,838** states, and the target `(E(G), empty)` is *not* among them. Script:
`notes/data/maskdp-8610/maskdp.py` (pure Python, ~25 min; prints the round-by-round closure;
the closure size plateaus from round 4).

Caveat: the search pairs only a Pareto-sorted beam (top 4000 states per round); the plateau is
strong machine evidence, not a proof, that no *tree* witness exists within 21 gates.

## The question

If L-meta-8610 is satisfiable at all, its witness must **share wires** (a DAG that is not any
tree of the same size) - a genuinely new shape for this band, unlike everything merged so far
for 8031-style packings. If it is unsatisfiable, the refutation needs a CDCL proof (four
encodings, ~10 core-hours of kissat/cadical at 20-40 min per instance, gave no verdict for 21
gates; the search is small - 67k clauses - but symmetries are brutal). The
`PEqualNP.Library.LRAT` machinery (genmono/genrow in `notes/data/lrat-link/`) formalizes such
a certificate, but note that `Link`'s normal-form clauses (source order, `used`, pad prefix)
are only satisfied by normal-form *models*, so bridging a table-form statement needs either a
normalization pass or a symmetry-free encoding.

*(end of note; the step's status at merge time of this note: still open)*
