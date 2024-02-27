# Midas Vergi Hesaplama

Bu uygulamanin kurumsal olarak Midas ile herhangi bir iliskisi yoktur.

## Web uzerinden hesaplama

Asagidaki sayfadan extreleri pdf olarak yukleyip hesaplama yapabilirsiniz. sonuc olarak bir excel dosyasi indiriyor olacaksiniz. Excel dosyasindaki son kolon islem basi ufe vs hesaplanarak vegiye tabi kazanci gosterecektir. 

[Midas Vergi Hesaplama ](http://hojuabi.polandcentral.cloudapp.azure.com:8000)

## Uyarilar

- Bu uygulama kisisel amacli olusturulmus olup baskalarinin da faydalanabilecegi hale getirildi ve acik kaynak kodlari https://github.com/hojuabi/midas adresinde bulunup kisisel kullanim amacli lokal olarak da calistirilabilir. 
- 2023 yili icinde yapilan butun satis islemleri adetlerinin alis tarihlerini iceren hesap ekstreleri(PDF) de eklenmelidir. 
- Islem bittiginde indirilecek Excel dosyasini actiginiz zaman en son kolon'da satis islemine karsilik gelen alis tarihi ve adetleri dikkate alinarak olusturulan vergiye tabi kazanci gorebilirsiniz. 
- Her ne kadar PDF kaydetme islemi yapilmiyor olsa da guvenliginiz icin PDF icindeki ozel bilgileri silmenin bir yolunu bulmanizda fayda var. Ben henuz bir yol bulamadim. 
-  **<ins>Hisse bolunmesi veya birlesmesi(split/reverse split) islemleri yeni eklendi. Ama ETF'ler icin listeyi bulamadim maalesef. Sonucta ortaya cikan Excel dosyasi uzerinde bunlari manuel olarak duzeltebilirsiniz</ins>**
- Hata bildirimi veya bilgi vs destek amaci ile hojuabi@gmail.com adresine yazabilirsiniz.

## Lokal calistirma

- Java ve pip kurulmus olmasi gerekiyor.
- Indirdikten sonra gerekli kutuphaneleri kurmak icin

` pip install -r requirements.txt`

- Sonra extreler(PDF)  ayni dizine kopyalanip asagidaki komut calistirilabilir. Bunun sonucunda ayni klasorde bir excel dosyasi olusacaktir.

`python3 calculate_tax.py`

