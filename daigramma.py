from graphviz import Digraph
import random

def generate_colors(n):
    """ Generate n distinct colors. """
    return ["#{:02x}{:02x}{:02x}".format(random.randint(110, 200), random.randint(110, 200), random.randint(0, 100)) for _ in range(n)]

def get_color():
    return "#{:02x}{:02x}{:02x}".format(random.randint(110, 200), random.randint(110, 200), random.randint(0, 100))


dot = Digraph(comment='Kļūdu Diagramma', engine='fdp', graph_attr={'rankdir': 'LR', 'splines': 'ortho', 'nodesep': '0.1', 'ranksep': '0.5'})
dot.attr(concentrate='true')
dot.attr('edge', label='')

# Add nodes
processes = ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10", "P11", "P12", "P13"]
# Define 'S' and 'F' nodes
S_nodes = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10"]
F_nodes = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"]

errors = ["E1", "E36", "E2", "E3", "E4", "E6", "E7", "E37", "E0", "E10", "E8", "E11", "E12", "E13", "E14", "E21", "E31", "E32", "E33", "E34", "E35", "E38"]

error_colors = generate_colors(len(errors))
for p in processes:
    dot.node(p, p)

for e, color in zip(errors, error_colors):
    dot.node(e, e, style='filled', color=color)


# for m in messages:
#     dot.node(m, m)


# Pievieno savienojumus (edges) starp darbībām un kļūdām
# dot.edge('P1', 'E1', 'Nav aizpildīts kāds lauks', color=get_color())
# dot.edge('P1', 'E36', 'Nepareiza lietotājvārda vai parole')
# dot.edge('P2', 'E1', 'Nav aizpildīts kāds lauks')
# dot.edge('P2', 'E2', 'Lietotājvārds jau aizņemts')
# dot.edge('P2', 'E3', 'Parole neatbilst prasībām')
# dot.edge('P3', 'E4', 'Nav aizpildīts lauks')
# dot.edge('P3', 'E6', 'Fails pārāk liels')
# dot.edge('P3', 'E7', 'E-pasts jau izmantots')
# dot.edge('P3', 'E37', 'Fails nav attēls')
# dot.edge('P4', 'E7', 'Nepareiza parole')
# dot.edge('P5', 'E4', 'Nav aizpildīts lauks')
# dot.edge('P5', 'E5', 'E-pasts nav derīgs')
# dot.edge('P5', 'E6', 'Fails pārāk liels')
# dot.edge('P5', 'E7', 'E-pasts jau izmantots')
# dot.edge('P6', 'E0', 'Sistēmas kļūda')
# dot.edge('P7', 'E10', 'Vecā parole ievadīta nepareizi')
# dot.edge('P7', 'E8', 'Jaunā parole neatbilst nosacījumiem')
# dot.edge('P7', 'E11', 'Jaunā parole sakrīt ar veco paroli')
# dot.edge('P8', 'E0', 'Sistēmas kļūda')
# dot.edge('P9', 'E12', 'Maksājuma kļūda')
# dot.edge('P10', 'E0', 'Sistēmas kļūda')
# dot.edge('P10', 'E10', 'Nepareiza parole')
# dot.edge('P11', 'E0', 'Sistēmas kļūda')
# dot.edge('P12', 'E0', 'Sistēmas kļūda')
# dot.edge('P13', 'E0', 'Sistēmas kļūda')
# dot.edge('S1', 'E21', 'Neizdevās iegūt GPS signālu')
# dot.edge('S1', 'E31', 'Nav pieejama stāvvietas informācija')
# dot.edge('S1', 'E0', 'Sistēmas kļūda')
# dot.edge('S2', 'E31', 'Nederīgi stāvvietas dati')
# dot.edge('S2', 'E0', 'Sistēmas kļūda')
# dot.edge('S3', 'E31', 'Nederīgi stāvvietas dati')
# dot.edge('S3', 'E0', 'Sistēmas kļūda')
# dot.edge('S4', 'E31', 'Nederīgi stāvvietas dati')
# dot.edge('S4', 'E0', 'Sistēmas kļūda')
# dot.edge('S5', 'E31', 'Nederīgi stāvvietas dati')
# dot.edge('S5', 'E0', 'Sistēmas kļūda')
# dot.edge('S6', 'E31', 'Nederīgi stāvvietas dati')
# dot.edge('S6', 'E0', 'Sistēmas kļūda')
# dot.edge('S7', 'E35', 'Nav atrasta neviena atbilstoša stāvvieta')
# dot.edge('S7', 'E0', 'Sistēmas kļūda')
# dot.edge('S8', 'E31', 'Nederīgi stāvvietas dati')
# dot.edge('S9', 'E32', 'Nederīgi stāvvietas dati')
# dot.edge('S9', 'E0', 'Sistēmas kļūda')
# dot.edge('S10', 'E32', 'Nederīgi stāvvietas dati')
# dot.edge('S10', 'E0', 'Sistēmas kļūda')
# dot.edge('F1', 'E14', 'Nederīgas lauka vērtības')
# dot.edge('E2', 'E4', 'Nav aizpildīts lauks')
# dot.edge('E2', 'E13', 'Nav privilēģijas')
# dot.edge('F3', 'E4', 'Nav aizpildīts lauks')
# dot.edge('F4', 'E1', 'Nav aizpildīts lauks')
# dot.edge('F5', 'E4', 'Nav aizpildīts lauks')
# dot.edge('F5', 'E38', 'Draugs jau grupā')
# dot.edge('F6', 'E21', 'Neizdevās iegūt GPS signālu')
# dot.edge('F7', 'E0', 'Sistēmas kļūda')
# dot.edge('F8', 'E14', 'Nederīgas lauka vērtības')
# dot.edge('F8', 'E0', 'Sistēmas kļūda')
# dot.edge('F9', 'E1', 'Nav aizpildīts lauks')
# dot.edge('F10', 'E14', 'Nederīgas lauka vērtības')
# dot.edge('F11', 'E14', 'Nederīgas lauka vērtības')
# dot.edge('F11', 'E33', 'Nav pieejama lietotāja informācija')
# dot.edge('F12', 'E33', 'Lietotājs nav atrasts')
# dot.edge('F12', 'E34', 'Statuss ir tāds pats')
# dot.edge('F12', 'E0', 'Sistēmas kļūda')

dot.edge('P1', 'E1', color=get_color())
dot.edge('P1', 'E36')
dot.edge('P2', 'E1')
dot.edge('P2', 'E2')
dot.edge('P2', 'E3')
dot.edge('P3', 'E4')
dot.edge('P3', 'E6')
dot.edge('P3', 'E7')
dot.edge('P3', 'E37')
dot.edge('P4', 'E7')
dot.edge('P5', 'E4')
dot.edge('P5', 'E5')
dot.edge('P5', 'E6')
dot.edge('P5', 'E7')
dot.edge('P6', 'E0')
dot.edge('P7', 'E10')
dot.edge('P7', 'E8')
dot.edge('P7', 'E11')
dot.edge('P8', 'E0')
dot.edge('P9', 'E12')
dot.edge('P10', 'E0')
dot.edge('P10', 'E10')
dot.edge('P11', 'E0')
dot.edge('P12', 'E0')
dot.edge('P13', 'E0')
dot.edge('S1', 'E21')
dot.edge('S1', 'E31')
dot.edge('S1', 'E0')
dot.edge('S2', 'E31')
dot.edge('S2', 'E0')
dot.edge('S3', 'E31')
dot.edge('S3', 'E0')
dot.edge('S4', 'E31')
dot.edge('S4', 'E0')
dot.edge('S5', 'E31')
dot.edge('S5', 'E0')
dot.edge('S6', 'E31')
dot.edge('S6', 'E0')
dot.edge('S7', 'E35')
dot.edge('S7', 'E0')
dot.edge('S8', 'E31')
dot.edge('S9', 'E32')
dot.edge('S9', 'E0')
dot.edge('S10', 'E32')
dot.edge('S10', 'E0')
dot.edge('F1', 'E14')
dot.edge('E2', 'E4')
dot.edge('E2', 'E13')
dot.edge('F3', 'E4')
dot.edge('F4', 'E1')
dot.edge('F5', 'E4')
dot.edge('F5', 'E38')
dot.edge('F6', 'E21')
dot.edge('F7', 'E0')
dot.edge('F8', 'E14')
dot.edge('F8', 'E0')
dot.edge('F9', 'E1')
dot.edge('F10', 'E14')
dot.edge('F11', 'E14')
dot.edge('F11', 'E33')
dot.edge('F12', 'E33')
dot.edge('F12', 'E34')
dot.edge('F12', 'E0')


# Add invisible edges to arrange nodes vertically
for i in range(len(processes)-1):
    dot.edge(processes[i], processes[i+1], style='invis')

# Add invisible edges for 'S' nodes
for i in range(len(S_nodes) - 1):
    dot.edge(S_nodes[i], S_nodes[i + 1], style='invis')

# Add invisible edges for 'F' nodes
for i in range(len(F_nodes) - 1):
    dot.edge(F_nodes[i], F_nodes[i + 1], style='invis')


for i in range(len(errors)-1):
    dot.edge(errors[i], errors[i+1], style='invis')

# Render the diagram to a file
dot.render('kļūdu_diagramma', format='png', cleanup=True)

# Renderē diagrammu uz failu
dot.render('kļūdu_diagramma', format='png', cleanup=True)
