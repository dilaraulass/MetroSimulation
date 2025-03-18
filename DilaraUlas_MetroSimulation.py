from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional
import networkx as nx
import matplotlib.pyplot as plt

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)

    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """BFS algoritması kullanarak en az aktarmalı rotayı bulur."""
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        kuyruk = deque([(baslangic, [baslangic])])
        ziyaret_edildi = set([baslangic])

        while kuyruk:
            mevcut_istasyon, rota = kuyruk.popleft()
            if mevcut_istasyon == hedef:
                return rota
            for komsu, _ in mevcut_istasyon.komsular:
                if komsu not in ziyaret_edildi:
                    ziyaret_edildi.add(komsu)
                    kuyruk.append((komsu, rota + [komsu]))

        return None

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """A* algoritması kullanarak en hızlı rotayı bulur."""
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        pq = [(0, id(baslangic), baslangic, [baslangic])]
        ziyaret_edildi = {}

        while pq:
            mevcut_sure, _, mevcut_istasyon, rota = heapq.heappop(pq)

            if mevcut_istasyon == hedef:
                return rota, mevcut_sure

            if mevcut_istasyon in ziyaret_edildi and ziyaret_edildi[mevcut_istasyon] <= mevcut_sure:
                continue

            ziyaret_edildi[mevcut_istasyon] = mevcut_sure

            for komsu, sure in mevcut_istasyon.komsular:
                yeni_sure = mevcut_sure + sure
                heapq.heappush(pq, (yeni_sure, id(komsu), komsu, rota + [komsu]))

        return None

    def metro_agini_gorsellestir(self):
        """Metro ağını NetworkX ve Matplotlib ile görselleştirir."""
        G = nx.Graph()

        # 1️⃣ İstasyonları düğüm olarak ekle
        for istasyon in self.istasyonlar.values():
            G.add_node(istasyon.idx, label=istasyon.ad, color=istasyon.hat)

        # 2️⃣ Bağlantıları kenar olarak ekle
        for istasyon in self.istasyonlar.values():
            for komsu, sure in istasyon.komsular:
                G.add_edge(istasyon.idx, komsu.idx, weight=sure)

        # 3️⃣ Grafiği çizmek için düğüm renklerini belirle
        renkler = {'Kırmızı Hat': 'red', 'Mavi Hat': 'blue', 'Turuncu Hat': 'orange'}
        node_colors = [renkler.get(G.nodes[n]['color'], 'gray') for n in G.nodes]

        # 4️⃣ Düğüm etiketlerini ve kenar ağırlıklarını belirle
        #pos = nx.spring_layout(G)  # Düğümleri düzenli yerleştir
        pos = nx.kamada_kawai_layout(G)  # Daha doğal yerleşim

        labels = {n: G.nodes[n]['label'] for n in G.nodes}
        edge_labels = {(u, v): d["weight"] for u, v, d in G.edges(data=True)}

        # 5️⃣ Grafiği çiz
        plt.figure(figsize=(10, 7))
        nx.draw(G, pos, with_labels=True, labels=labels, node_size=2000, node_color=node_colors, font_size=10, font_weight="bold", edge_color="gray")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

        plt.title("Metro Ağı Görselleştirme")
        plt.show()

# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    metro.baglanti_ekle("K1", "K2", 4)
    metro.baglanti_ekle("K2", "K3", 6)
    metro.baglanti_ekle("K3", "K4", 8)
    
    metro.baglanti_ekle("M1", "M2", 5)
    metro.baglanti_ekle("M2", "M3", 3)
    metro.baglanti_ekle("M3", "M4", 4)
    
    metro.baglanti_ekle("T1", "T2", 7)
    metro.baglanti_ekle("T2", "T3", 9)
    metro.baglanti_ekle("T3", "T4", 5)
    
    metro.baglanti_ekle("K1", "M2", 2)
    metro.baglanti_ekle("K3", "T2", 3)
    metro.baglanti_ekle("M4", "T3", 2)
    
    # Görselleştirme
    metro.metro_agini_gorsellestir()
  # Test Senaryoları
    print("\n=== Test Senaryoları ===")
    
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))