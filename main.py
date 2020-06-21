# import library numpy untuk mempermudah komputasi saintifik
import numpy as np
# dari Python Image Library (PIL) import ImageTk dan Image
from PIL import ImageTk, Image
# dari collections import Counter untuk meghitung banyak kemunculan data
from collections import Counter
# tkinter adalah libary GUI untuk python
from tkinter import Tk, Button, filedialog, Label, Canvas, Message
# KMeans adalah algoritma klusterisasi, dalam projet ini digunakan untuk mengelompokkan warna
from sklearn.cluster import KMeans
# Untuk mengambil titik tengah yang mewakili kluster warna
from sklearn.neighbors import NearestCentroid

# deklarasi panel untuk menampilkan foto, warna dominan, 
# dan pesan teks terkait persentase warna dominan
panel_photo = None
panel_canvas = None
panel_message = None
# fungsi untuk membuka, menampilkan gambar, menampilkan warna dominan dan persentasenya
def open_img_and_draw():
    # panjang
    w = 480
    # lebar
    h = 360
    # mendeklarasikan panel yang sudah dideklarasikan menjadi global
    global panel_photo, panel_canvas, panel_message
    # jika fungsi open_img_and_draw() sudah dijalankan sebelumnya
    # maka tutup / hapus panel yang sudah ada sebelumnya
    if panel_photo != None:
        panel_photo.destroy()
        panel_canvas.destroy()
        panel_message.destroy()
    
    # tampilkan jendela untuk memilih file gambar yang akan diproses
    x = openfilename() 
    # simpan file sebagai gambar
    img = Image.open(x)
    # ubah ukuran gambar sesuai panjang dan lebar yg telah ditentukan
    img = img.resize((w, h), Image.ANTIALIAS)
    # ambil 3 warna dominan dan total kemunculan dari 3 warna dominan
    # bisa menggunakan algoritam klusterisasi KMeans atau hanya dengan 
    # mengurutkan kemunculan rgb yang paling banyak muncul digambar
    top_3_colors, top_3_total_colors = frequent_3_colors(img, 'kmeans')
    # ubah gambar menjadi gambar untuk GUI
    img = ImageTk.PhotoImage(img)
    # tampilkan gambar di panel_photo
    panel_photo = Label(root, image=img) 
    panel_photo.image = img 
    # letakkan panel_photo dengan mengisi dari sisi kiri
    panel_photo.pack(side='left')

    # deklarasi canvas untuk menggambar warna dominan
    panel_canvas = Canvas(root)
    # buat kotak pada dengan ujung atas kiri x=30, y=10 dan ujung bawah kanan x=120, y=80
    # dengan warna pertama dari 3 warna dominan, dan seterusnya
    panel_canvas.create_rectangle(30, 10, 120, 80, fill=rgb_to_hex(top_3_colors[0]))
    panel_canvas.create_rectangle(150, 10, 240, 80, fill=rgb_to_hex(top_3_colors[1]))
    panel_canvas.create_rectangle(270, 10, 360, 80, fill=rgb_to_hex(top_3_colors[2]))
    # letakkan panel_canvas dengan mengisi dari sisi kiri
    panel_canvas.pack(side='left')

    # hitung persentase warna dominan
    top_3_percentage_colors = []
    # loop 3 kali karena ada 3 warna
    for i in range(3):
        # total kemunculan warna / (panjang * lebar) * 100 persen,
        # lalu masukkan ke list top_3_percentage_colors
        top_3_percentage_colors.append((top_3_total_colors[i] / (w * h)) * 100)
    
    # deklarasi panel_message untuk menampilkan persentase warna dominan
    panel_message = Message(root, 
        text='Color 1: {:.2f}%\nColor 2: {:.2f}%\nColor 3: {:.2f}%'.format(
            top_3_percentage_colors[0], top_3_percentage_colors[1], top_3_percentage_colors[2]))
    # letakkan panel_message dengan mengisi dari sisi kiri
    panel_message.pack(side='left')

# fungsi untuk menampilkan jendela untuk memilih file gambar yang akan diproses
def openfilename(): 
    filename = filedialog.askopenfilename(title ='Select Image') 
    
    return filename

# fungsi untuk mendapatkan 3 warna dominan
def frequent_3_colors(image, method):
    # deklarasi list untuk menampung rgb 3 warna dominan
    top_3_colors = []
    # deklarasi list untuk menampung kemunculan rgb 3 warna dominan(jika menggunakan sort)
    # atau menampung banyak anggota kluster dari klusterisasi warna dominan(metode KMeans)
    top_3_total_colors = []
    if method == 'kmeans':
        # ubah gambar yg sebelumnya berformat RGBA menjadi RGB
        # lalu ambil informasi RGB tiap piksel
        list_rgb = np.array(image.convert('RGB').getdata(), dtype=np.uint8)
        # lakukan klusterisasi terhadap RGB tiap piksel dengan 3 kluster
        cluster = KMeans(n_clusters=3, random_state=1).fit(list_rgb)
        # ambil titik tengah / centroid dari 3 kluster
        clf = NearestCentroid().fit(list_rgb, cluster.labels_)
        top_3_colors = clf.centroids_
        # hitung banyak anggota tiap kluster
        cluster_total_member = Counter(cluster.labels_).values()
        # urutkan berdasar anggota kluster yang paling banyak
        top_3_total_colors = sorted(cluster_total_member, reverse=True)
    elif method == 'sort':
        # ambil panjang dan lebar gambar
        w, h = image.size
        # ubah gambar dari RGBA menjadi RBG lalu ambil total kemunculan RGB dan nilai RGBnya
        pixels = image.convert('RGB').getcolors(w * h)
        # urutkan berdasar kemunculan RGB yang paling banyak
        sort_occurence_colors = sorted(pixels, key=lambda x:x[0], reverse=True)
        # masukkan 3 RGB dan total kemunculannya di list yang telah dideklarasikan
        for i in range(3):
            top_3_colors.append(sort_occurence_colors[i][1])
            top_3_total_colors.append(sort_occurence_colors[i][0])
    else:
        return None
    
    return top_3_colors, top_3_total_colors

# ubah warna rgb jadi heksadesimal
def rgb_to_hex(color):
    return '#{0:02x}{1:02x}{2:02x}'.format(int(color[0]), int(color[1]), int(color[2]))

# deklarasi GUI
root = Tk()
# deklarasi judul GUI
root.title('Dominant Color Getter')
# deklarasi ukuran GUI
root.geometry('1000x480') 
# deklarasi apakah GUI panjang lebar GUI bisa diubah ukurannya
root.resizable(width = True, height = True) 
# deklarasi tombol untuk membuka gambar dan memprosesnya lalu letakkan ditengah
btn = Button(root, text ='Open Image', command = open_img_and_draw).pack()
# tampilkan GUI secara terus menerus selama tidak ditutup
root.mainloop()