from py_ecc.bn128 import FQ, is_on_curve, b, curve_order, multiply, add, G1, G2
from galois import GF, Poly

GF = GF(curve_order, primitive_element=5, verify=False)
main_discrete_log = 100
alpha_discrete_log = 101
beta_discrete_log = 102
gamma_discrete_log = 103
delta_discrete_log = 104

v1 = Poly([1, (-1) % curve_order], field=GF)
v2 = Poly([1, (-2) % curve_order], field=GF)
v3 = Poly([1, (-3) % curve_order], field=GF)
vanishing = v1*v2*v3
evaluated_poly = vanishing(100)

g1_vector = []
for i in range(3):
    g1_vector.append(
        multiply(G1, main_discrete_log**i)
    )
# print(g1_vector)

ht_vector = []
delta_neg = int(-GF(delta_discrete_log))
multiplier = int(GF(evaluated_poly) * delta_neg)
for i in range(3):
    ht_vector.append(
        multiply(g1_vector[i], multiplier)
    )

print(ht_vector)

# g1_points = 
# print(v1)
# print(v2)
# print(v3)
# print(v1*v2*v3)
# assert v1(1) == 0
# assert v2(2) == 0
# assert v3(3) == 0

# x^3 + 21888242871839275222246405745257275088548364400416034343698204186575808495611x^2 + 11x + 21888242871839275222246405745257275088548364400416034343698204186575808495611


# private =  [(7958921442153461540529327299999974550179228871339307524420969495322266309190, 21430513512845629241976885987655757293297088138979534880443747135546018572372), (17895810394707652193166392852157039960066841948428569660629397271914977401986, 19504059296190346458448929110060268585061500992420889025620925616197854868804), (10055249679538384873934190386509166933933129073220983833920255521621805497796, 1745887576635150795987083512526488797562027813682340233346619771405922541199)]
# witness =  [1, 3049703, 100, 100, 30000, 3000000]
# # points = [(FQ(x), FQ(y), FQ(1)) for x, y in private]

# points = [(FQ(x), FQ(y)) for x, y in private]

# result = add(
#     add(
#         multiply(points[0], witness[3]),
#         multiply(points[1], witness[4])
#     ),
#     multiply(points[2], witness[5])
# )
# print(result)