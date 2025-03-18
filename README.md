# 🏙️ Metro Ağ Simülasyonu 🚇

Bu proje, bir metro ağı için **rota bulma ve görselleştirme** işlemlerini gerçekleştiren bir Python uygulamasıdır.  
BFS (Genişlik Öncelikli Arama)** algoritması ile **en az aktarmalı rota** bulunur,  
A* algoritması** ile **en hızlı yol** hesaplanır ve  metro ağı **grafik olarak görselleştirilir.**
---
import heapq -> heapq(öncelik kuyruğu) en küçük veya en büyük öğeyi hızla almak için kullanılır. A* algoritması ve en kısa yol hesaplamaları için idealdir.
import networkx as nx -> graf (graph) veri yapıları oluşturmak ve bağlantıları modellemek için kullanılır.
import matplotlib.pyplot as plt -> matplotlib veri görselleştirmek için pyplot grafik çizimi için kullanılır
---

## 🚀 **Özellikler**
✅ Metro istasyonlarını ekleyip yönetebilme  
✅ **En az aktarma** yapan rotayı bulma (**BFS**)  
✅ **En hızlı rotayı** hesaplama (**A* Algoritması**)  
✅ **Metro ağını çizerek görselleştirme**  
✅ **Test senaryoları** ile rotaların çalışmasını kontrol etme  


**BFS Algoritmasının Çalışma Mantığı**
Başlangıç düğümü kuyruk içine alınır.
Kuyruk boş değilken şu adımlar tekrar edilir:
Ön sıradaki düğüm çıkarılır (dequeue).
Bu düğüm ziyaret edilmiş olarak işaretlenir.
Bu düğüme komşu olan ve daha önce ziyaret edilmemiş tüm düğümler kuyruğa eklenir (enqueue).
BFS, önce tüm aynı seviyedeki düğümleri ziyaret ettiği için en kısa yolu bulmak için uygundur

**A Algoritmasının Çalışma Mantığı**
Dijkstra ve Best-First Search (BFS + Heuristic) mantığını birleştirerek en hızlı rotayı bulur.
A* algoritması bir öncelik kuyruğu (priority queue) kullanarak en hızlı yolu bulur.
Her düğüm (node) için toplam maliyeti (f) hesaplar.
Amaç: Her seferinde en düşük f(n) değerine sahip düğümü seçmektir!

