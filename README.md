# Midas Vergi Hesaplama

Bu uygulamanin kurumsal olarak Midas ile herhangi bir iliskisi yoktur.

## Web uzerinden hesaplama

Asagidaki sayfadan extreleri pdf olarak yukleyip hesaplama yapabilirsiniz. sonuc olarak bir excel dosyasi indiriyor olacaksiniz.

[Midas Vergi Hesaplama ](http://hojuabi.polandcentral.cloudapp.azure.com:8000)

## Uyarilar

-Bu uygulama kisisel amacli olusturulmus olup baskalarinin da faydalanabilecegi hale getirildi ve acik kaynak kodlari https://github.com/hojuabi/midas adresinde bulunup kisisel kullanim amacli lokal olarak da calistirilabilir. 
-2023 yili icinde yapilan butun satis islemleri adetlerinin alis tarihlerini iceren hesap ekstreleri(PDF) de eklenmelidir. 
-Islem bittiginde indirilecek Excel dosyasini actiginiz zaman en son kolon'da satis islemine karsilik gelen alis tarihi ve adetleri dikkate alinarak olusturulan vergiye tabi kazanci gorebilirsiniz. 
-Her ne kadar PDF kaydetme islemi yapilmiyor olsa da guvenliginiz icin PDF icindeki ozel bilgileri silmenin bir yolunu bulmanizda fayda var. Ben henuz bir yol bulamadim. 
-Hisse bolunmesi veya birlesmesi(split/reverse split) islemleri uzerinde calisiyorum. Ama ETF'ler icin listeyi bulamadim maalesef. Sonucta ortaya cikan Excel dosyasi uzerinde bunlari manuel olarak duzeltebilirsiniz. 
-Hata bildirimi veya bilgi vs destek amaci ile hojuabi@gmail.com adresine yazabilirsiniz.

## Lokal calistirma

Indirdikten sonra gerekli kutuphaneler pip ile kurulduktan sonra extreler(PDF) olarak ayni dizine kopyalanip pytho3 calculate_tax.py komutu ile claistirilabilir. Bunun sonucunda ayni klasorde bir excel dosyasi olusacaktir.
