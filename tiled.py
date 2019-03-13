import os
import xml.etree.ElementTree as ET
import array2d

#########################
# Tiledのデータを扱う注意点
# 何もないデータは "0" となります
# そのためデータは "1" 始まりです
#########################

# Tiled Map Editor読み込みクラス
class Tiled:
    def __init__(self, path=""):
        if path != "":
            self.load(path)
    def load(self, path):
        # *.tmx ファイル読み込み
        elem = ET.parse(path)
        root = elem.getroot()
        self.name       = os.path.basename(path)
        self.width      = int(root.get("width"))
        self.height     = int(root.get("height"))
        self.tilewidth  = int(root.get("tilewidth"))
        self.tileheight = int(root.get("tileheight"))
        self.layers = []
        for child in root:
            if child.tag == "layer":
                w = int(child.get("width"))
                h = int(child.get("height"))
                layer = array2d.Array2D(w, h)
                for data in child:
                    if data.tag == "data":
                        idx = 0
                        text = data.text
                        for line in text.split("\n"):
                            for v in line.split(","):
                                if v.strip() == "":
                                    break
                                layer.set_from_idx(idx, int(v))
                                idx += 1
                self.layers.append(layer)

    def dump(self):
        # デバッグ出力
        print("Tiled dump.")
        print("filename = %s"%self.name)
        print("(width, height) = (%d, %d)"%(self.width, self.height))
        print("(tile_width, tile_height) = (%d, %d)"%(self.tilewidth, self.tileheight))
        for i, layer in enumerate(self.layers):
            print("layer[%d] (width, height) = (%d, %d)"%(i, layer.width, layer.height))
            layer.dump()
