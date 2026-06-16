import numpy as np
import matplotlib.pyplot as plt

# Data eksperimen
x_exp = np.array([8,16,24,32])
y_exp = np.array([0.700,-0.775,-1.000,0.425])

# Data teori titik pengukuran
y_teori_titik = np.array([0.188,-1.000,-1.000,0.188])

# Kurva teori Euler-Bernoulli (dibuat smooth)
x_teori = np.linspace(0,40,500)

# Kurva aproksimasi sesuai gambar
coef = np.polyfit(
    [0,8.97,20,31.03,40],
    [1,0,-0.6,0,1],
    4
)

y_teori = np.polyval(coef,x_teori)

# Plot
plt.figure(figsize=(10,6))

# Kurva teori
plt.plot(x_teori,y_teori,
         'b-',linewidth=2,
         label='Teori Euler-Bernoulli (kontinu)')

# Titik teori
plt.plot(x_exp,y_teori_titik,
         'bs',markersize=10,
         markerfacecolor='white',
         markeredgewidth=2,
         label='Teori (titik pengukuran)')

# Eksperimen
plt.plot(x_exp,y_exp,
         'ro-',linewidth=2,
         markersize=10,
         label='Eksperimen')

# Node
plt.axvline(8.97,color='purple',
            linestyle=':',alpha=0.7)

plt.axvline(31.03,color='purple',
            linestyle=':',alpha=0.7,
            label='Node (φ=0)')

# Garis nol
plt.axhline(0,color='black')

# Anotasi deviasi
for x,t,e in zip(x_exp,y_teori_titik,y_exp):
    plt.annotate(
        f'Δ={e-t:+.3f}',
        xy=(x,e),
        xytext=(x+1,(e+t)/2),
        arrowprops=dict(arrowstyle='->')
    )

plt.text(29,0.95,
         'MAC = 0.839',
         color='darkred',
         fontsize=12,
         bbox=dict(facecolor='white'))

plt.xlabel('Posisi x (cm)',fontsize=12)
plt.ylabel('Amplitudo Mode Shape (norm.)',fontsize=12)

plt.title('Perbandingan Mode Shape Modus Pertama\nEksperimen vs Prediksi Euler-Bernoulli')

plt.grid(True,alpha=0.3)
plt.legend()
plt.xlim(0,40)
plt.ylim(-1.2,1.2)

plt.show()