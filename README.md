# 🧠 Wittgenstein's *Tractatus* Graph Visualisation

An **interactive network graph** of Ludwig Wittgenstein’s *Tractatus Logico-Philosophicus* (1921), where  
- 🟦 **Nodes** represent numbered propositions (e.g. `2.1`, `3.143`, etc.)  
- ➡️ **Edges** encode Wittgenstein’s **parent–child logical structure**  
- ⌨️ **Keyboard navigation** allows you to traverse the text as Wittgenstein intended (depth-first order)  
- 💬 **Tooltips** display the text of each proposition on hover

> ✨ This project bridges **philosophical logic**, **graph theory**, and **interactive data visualisation**, demonstrating how structured texts can be explored computationally.

![Tractatus Graph Screenshot](./docs/screenshot.png)

---

## 🌐 Live Demo

👉 **[View the interactive graph](https://ChloeMYWong.github.io/tractatus-graph-visualisation/tractatus_network2.html)**  
(*Hosted with GitHub Pages*)

---

## 🛠️ Features

- **Graph Structure**
  - Directed graph built using [`networkx`](https://networkx.org/)
  - Rendered interactively with [`pyvis`](https://pyvis.readthedocs.io/en/latest/) and [`vis-network`](https://visjs.github.io/vis-network/)
  - Colour-coded nodes by **depth** in the tree

- **Keyboard Controls**
  - `→` / `←` Traverse forward/back through propositions in book order  
  - `↑` Zoom to current node  
  - `↓` Reset zoom  
  - `Enter` Toggle highlight mode  

- **Tooltips & Interaction**
  - Hover over nodes to view the proposition text
  - Click to highlight local neighbourhoods

---

## 🧪 Quick Start

You can run the project locally in just a few steps:

### 1️⃣ Clone the repository
```bash
git clone https://github.com/USERNAME/tractatus-graph-visualisation.git
cd tractatus-graph-visualisation
# tractatus-graph-visualisation
