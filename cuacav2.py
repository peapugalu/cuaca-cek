import requests
from datetime import datetime, timedelta
from collections import defaultdict

class WeatherAnalyzerIndonesia:
    def __init__(self):
        self.provinces = {
            "Aceh": {
                "ibukota": "Banda Aceh",
                "kabupaten_kota": [
                    "Kabupaten Aceh Barat", "Kabupaten Aceh Barat Daya", "Kabupaten Aceh Besar",
                    "Kabupaten Aceh Jaya", "Kabupaten Aceh Selatan", "Kabupaten Aceh Singkil",
                    "Kabupaten Aceh Tamiang", "Kabupaten Aceh Tengah", "Kabupaten Aceh Tenggara",
                    "Kabupaten Aceh Timur", "Kabupaten Aceh Utara", "Kabupaten Bener Meriah",
                    "Kabupaten Bireuen", "Kabupaten Gayo Lues", "Kabupaten Nagan Raya",
                    "Kabupaten Pidie", "Kabupaten Pidie Jaya", "Kabupaten Simeulue",
                    "Kota Banda Aceh", "Kota Langsa", "Kota Lhokseumawe", "Kota Sabang",
                    "Kota Subulussalam"
                ]
            },
            "Sumatera Utara": {
                "ibukota": "Medan",
                "kabupaten_kota": [
                    "Kabupaten Asahan", "Kabupaten Batubara", "Kabupaten Dairi",
                    "Kabupaten Deli Serdang", "Kabupaten Humbang Hasundutan", "Kabupaten Karo",
                    "Kabupaten Labuhanbatu", "Kabupaten Labuhanbatu Selatan", "Kabupaten Labuhanbatu Utara",
                    "Kabupaten Langkat", "Kabupaten Mandailing Natal", "Kabupaten Nias",
                    "Kabupaten Nias Barat", "Kabupaten Nias Selatan", "Kabupaten Nias Utara",
                    "Kabupaten Padang Lawas", "Kabupaten Padang Lawas Utara", "Kabupaten Pakpak Bharat",
                    "Kabupaten Samosir", "Kabupaten Serdang Bedagai", "Kabupaten Simalungun",
                    "Kabupaten Tapanuli Selatan", "Kabupaten Tapanuli Tengah", "Kabupaten Tapanuli Utara",
                    "Kabupaten Toba Samosir",
                    "Kota Binjai", "Kota Gunungsitoli", "Kota Medan", "Kota Padang Sidempuan",
                    "Kota Pematangsiantar", "Kota Sibolga", "Kota Tanjungbalai", "Kota Tebing Tinggi"
                ]
            },
            "Sumatera Barat": {
                "ibukota": "Padang",
                "kabupaten_kota": [
                    "Kabupaten Agam", "Kabupaten Dharmasraya", "Kabupaten Kepulauan Mentawai",
                    "Kabupaten Lima Puluh Kota", "Kabupaten Padang Pariaman", "Kabupaten Pasaman",
                    "Kabupaten Pasaman Barat", "Kabupaten Pesisir Selatan", "Kabupaten Sijunjung",
                    "Kabupaten Solok", "Kabupaten Solok Selatan", "Kabupaten Tanah Datar",
                    "Kota Bukittinggi", "Kota Padang", "Kota Padang Panjang", "Kota Pariaman",
                    "Kota Payakumbuh", "Kota Sawahlunto", "Kota Solok"
                ]
            },
            "Riau": {
                "ibukota": "Pekanbaru",
                "kabupaten_kota": [
                    "Kabupaten Bengkalis", "Kabupaten Indragiri Hilir", "Kabupaten Indragiri Hulu",
                    "Kabupaten Kampar", "Kabupaten Kepulauan Meranti", "Kabupaten Kuantan Singingi",
                    "Kabupaten Pelalawan", "Kabupaten Rokan Hilir", "Kabupaten Rokan Hulu",
                    "Kabupaten Siak", "Kota Dumai", "Kota Pekanbaru"
                ]
            },
            "Kepulauan Riau": {
                "ibukota": "Tanjung Pinang",
                "kabupaten_kota": [
                    "Kabupaten Bintan", "Kabupaten Karimun", "Kabupaten Kepulauan Anambas",
                    "Kabupaten Lingga", "Kabupaten Natuna", "Kota Batam", "Kota Tanjung Pinang"
                ]
            },
            "Jambi": {
                "ibukota": "Jambi",
                "kabupaten_kota": [
                    "Kabupaten Batanghari", "Kabupaten Bungo", "Kabupaten Kerinci",
                    "Kabupaten Merangin", "Kabupaten Muaro Jambi", "Kabupaten Sarolangun",
                    "Kabupaten Tanjung Jabung Barat", "Kabupaten Tanjung Jabung Timur", "Kabupaten Tebo",
                    "Kota Jambi", "Kota Sungai Penuh"
                ]
            },
            "Sumatera Selatan": {
                "ibukota": "Palembang",
                "kabupaten_kota": [
                    "Kabupaten Banyuasin", "Kabupaten Empat Lawang", "Kabupaten Lahat",
                    "Kabupaten Muara Enim", "Kabupaten Musi Banyuasin", "Kabupaten Musi Rawas",
                    "Kabupaten Musi Rawas Utara", "Kabupaten Ogan Ilir", "Kabupaten Ogan Komering Ilir",
                    "Kabupaten Ogan Komering Ulu", "Kabupaten Ogan Komering Ulu Selatan", "Kabupaten Ogan Komering Ulu Timur",
                    "Kabupaten Penukal Abab Lematang Ilir", "Kota Lubuklinggau", "Kota Pagar Alam",
                    "Kota Palembang", "Kota Prabumulih"
                ]
            },
            "Bangka Belitung": {
                "ibukota": "Pangkal Pinang",
                "kabupaten_kota": [
                    "Kabupaten Bangka", "Kabupaten Bangka Barat", "Kabupaten Bangka Selatan",
                    "Kabupaten Bangka Tengah", "Kabupaten Belitung", "Kabupaten Belitung Timur",
                    "Kota Pangkal Pinang"
                ]
            },
            "Bengkulu": {
                "ibukota": "Bengkulu",
                "kabupaten_kota": [
                    "Kabupaten Bengkulu Selatan", "Kabupaten Bengkulu Tengah", "Kabupaten Bengkulu Utara",
                    "Kabupaten Kaur", "Kabupaten Kepahiang", "Kabupaten Lebong",
                    "Kabupaten Mukomuko", "Kabupaten Rejang Lebong", "Kabupaten Seluma",
                    "Kota Bengkulu"
                ]
            },
            "Lampung": {
                "ibukota": "Bandar Lampung",
                "kabupaten_kota": [
                    "Kabupaten Lampung Barat", "Kabupaten Lampung Selatan", "Kabupaten Lampung Tengah",
                    "Kabupaten Lampung Timur", "Kabupaten Lampung Utara", "Kabupaten Mesuji",
                    "Kabupaten Pesawaran", "Kabupaten Pesisir Barat", "Kabupaten Pringsewu",
                    "Kabupaten Tanggamus", "Kabupaten Tulang Bawang", "Kabupaten Tulang Bawang Barat",
                    "Kabupaten Way Kanan", "Kota Bandar Lampung", "Kota Metro"
                ]
            },
            "DKI Jakarta": {
                "ibukota": "Jakarta",
                "kabupaten_kota": [
                    "Kota Jakarta Barat", "Kota Jakarta Pusat", "Kota Jakarta Selatan",
                    "Kota Jakarta Timur", "Kota Jakarta Utara", "Kabupaten Kepulauan Seribu"
                ]
            },
            "Jawa Barat": {
                "ibukota": "Bandung",
                "kabupaten_kota": [
                    "Kabupaten Bandung", "Kabupaten Bandung Barat", "Kabupaten Bekasi",
                    "Kabupaten Bogor", "Kabupaten Ciamis", "Kabupaten Cianjur",
                    "Kabupaten Cirebon", "Kabupaten Garut", "Kabupaten Indramayu",
                    "Kabupaten Karawang", "Kabupaten Kuningan", "Kabupaten Majalengka",
                    "Kabupaten Pangandaran", "Kabupaten Purwakarta", "Kabupaten Subang",
                    "Kabupaten Sukabumi", "Kabupaten Sumedang", "Kabupaten Tasikmalaya",
                    "Kota Bandung", "Kota Banjar", "Kota Bekasi", "Kota Bogor",
                    "Kota Cimahi", "Kota Cirebon", "Kota Depok", "Kota Sukabumi", "Kota Tasikmalaya"
                ]
            },
            "Banten": {
                "ibukota": "Serang",
                "kabupaten_kota": [
                    "Kabupaten Lebak", "Kabupaten Pandeglang", "Kabupaten Serang",
                    "Kabupaten Tangerang", "Kota Cilegon", "Kota Serang",
                    "Kota Tangerang", "Kota Tangerang Selatan"
                ]
            },
            "Jawa Tengah": {
                "ibukota": "Semarang",
                "kabupaten_kota": [
                    "Kabupaten Banjarnegara", "Kabupaten Banyumas", "Kabupaten Batang",
                    "Kabupaten Blora", "Kabupaten Boyolali", "Kabupaten Brebes",
                    "Kabupaten Cilacap", "Kabupaten Demak", "Kabupaten Grobogan",
                    "Kabupaten Jepara", "Kabupaten Karanganyar", "Kabupaten Kebumen",
                    "Kabupaten Kendal", "Kabupaten Klaten", "Kabupaten Kudus",
                    "Kabupaten Magelang", "Kabupaten Pati", "Kabupaten Pekalongan",
                    "Kabupaten Pemalang", "Kabupaten Purbalingga", "Kabupaten Purworejo",
                    "Kabupaten Rembang", "Kabupaten Semarang", "Kabupaten Sragen",
                    "Kabupaten Sukoharjo", "Kabupaten Tegal", "Kabupaten Temanggung",
                    "Kabupaten Wonogiri", "Kabupaten Wonosobo",
                    "Kota Magelang", "Kota Pekalongan", "Kota Salatiga", "Kota Semarang", "Kota Surakarta", "Kota Tegal"
                ]
            },
            "DI Yogyakarta": {
                "ibukota": "Yogyakarta",
                "kabupaten_kota": [
                    "Kabupaten Bantul", "Kabupaten Gunungkidul", "Kabupaten Kulon Progo",
                    "Kabupaten Sleman", "Kota Yogyakarta"
                ]
            },
            "Jawa Timur": {
                "ibukota": "Surabaya",
                "kabupaten_kota": [
                    "Kabupaten Bangkalan", "Kabupaten Banyuwangi", "Kabupaten Blitar",
                    "Kabupaten Bojonegoro", "Kabupaten Bondowoso", "Kabupaten Gresik",
                    "Kabupaten Jember", "Kabupaten Jombang", "Kabupaten Kediri",
                    "Kabupaten Lamongan", "Kabupaten Lumajang", "Kabupaten Madiun",
                    "Kabupaten Magetan", "Kabupaten Malang", "Kabupaten Mojokerto",
                    "Kabupaten Nganjuk", "Kabupaten Ngawi", "Kabupaten Pacitan",
                    "Kabupaten Pamekasan", "Kabupaten Pasuruan", "Kabupaten Ponorogo",
                    "Kabupaten Probolinggo", "Kabupaten Sampang", "Kabupaten Sidoarjo",
                    "Kabupaten Situbondo", "Kabupaten Sumenep", "Kabupaten Trenggalek",
                    "Kabupaten Tuban", "Kabupaten Tulungagung",
                    "Kota Batu", "Kota Blitar", "Kota Kediri", "Kota Madiun", "Kota Malang",
                    "Kota Mojokerto", "Kota Pasuruan", "Kota Probolinggo", "Kota Surabaya"
                ]
            },
            "Bali": {
                "ibukota": "Denpasar",
                "kabupaten_kota": [
                    "Kabupaten Badung", "Kabupaten Bangli", "Kabupaten Buleleng",
                    "Kabupaten Gianyar", "Kabupaten Jembrana", "Kabupaten Karangasem",
                    "Kabupaten Klungkung", "Kabupaten Tabanan", "Kota Denpasar"
                ]
            },
            "Nusa Tenggara Barat": {
                "ibukota": "Mataram",
                "kabupaten_kota": [
                    "Kabupaten Bima", "Kabupaten Dompu", "Kabupaten Lombok Barat",
                    "Kabupaten Lombok Tengah", "Kabupaten Lombok Timur", "Kabupaten Lombok Utara",
                    "Kabupaten Sumbawa", "Kabupaten Sumbawa Barat", "Kota Bima", "Kota Mataram"
                ]
            },
            "Nusa Tenggara Timur": {
                "ibukota": "Kupang",
                "kabupaten_kota": [
                    "Kabupaten Alor", "Kabupaten Belu", "Kabupaten Ende",
                    "Kabupaten Flores Timur", "Kabupaten Kupang", "Kabupaten Lembata",
                    "Kabupaten Malaka", "Kabupaten Manggarai", "Kabupaten Manggarai Barat",
                    "Kabupaten Manggarai Timur", "Kabupaten Nagekeo", "Kabupaten Ngada",
                    "Kabupaten Rote Ndao", "Kabupaten Sabu Raijua", "Kabupaten Sikka",
                    "Kabupaten Sumba Barat", "Kabupaten Sumba Barat Daya", "Kabupaten Sumba Tengah",
                    "Kabupaten Sumba Timur", "Kabupaten Timor Tengah Selatan", "Kabupaten Timor Tengah Utara",
                    "Kota Kupang"
                ]
            },
            "Kalimantan Barat": {
                "ibukota": "Pontianak",
                "kabupaten_kota": [
                    "Kabupaten Bengkayang", "Kabupaten Kapuas Hulu", "Kabupaten Kayong Utara",
                    "Kabupaten Ketapang", "Kabupaten Kubu Raya", "Kabupaten Landak",
                    "Kabupaten Melawi", "Kabupaten Mempawah", "Kabupaten Sambas",
                    "Kabupaten Sanggau", "Kabupaten Sekadau", "Kabupaten Sintang",
                    "Kota Pontianak", "Kota Singkawang"
                ]
            },
            "Kalimantan Tengah": {
                "ibukota": "Palangka Raya",
                "kabupaten_kota": [
                    "Kabupaten Barito Selatan", "Kabupaten Barito Timur", "Kabupaten Barito Utara",
                    "Kabupaten Gunung Mas", "Kabupaten Kapuas", "Kabupaten Katingan",
                    "Kabupaten Kotawaringin Barat", "Kabupaten Kotawaringin Timur", "Kabupaten Lamandau",
                    "Kabupaten Murung Raya", "Kabupaten Pulang Pisau", "Kabupaten Sukamara",
                    "Kabupaten Seruyan", "Kota Palangka Raya"
                ]
            },
            "Kalimantan Selatan": {
                "ibukota": "Banjarmasin",
                "kabupaten_kota": [
                    "Kabupaten Balangan", "Kabupaten Banjar", "Kabupaten Barito Kuala",
                    "Kabupaten Hulu Sungai Selatan", "Kabupaten Hulu Sungai Tengah", "Kabupaten Hulu Sungai Utara",
                    "Kabupaten Kotabaru", "Kabupaten Tabalong", "Kabupaten Tanah Bumbu",
                    "Kabupaten Tanah Laut", "Kabupaten Tapin", "Kota Banjarbaru", "Kota Banjarmasin"
                ]
            },
            "Kalimantan Timur": {
                "ibukota": "Samarinda",
                "kabupaten_kota": [
                    "Kabupaten Berau", "Kabupaten Kutai Barat", "Kabupaten Kutai Kartanegara",
                    "Kabupaten Kutai Timur", "Kabupaten Mahakam Ulu", "Kabupaten Paser",
                    "Kabupaten Penajam Paser Utara", "Kota Balikpapan", "Kota Bontang", "Kota Samarinda"
                ]
            },
            "Kalimantan Utara": {
                "ibukota": "Tanjung Selor",
                "kabupaten_kota": [
                    "Kabupaten Bulungan", "Kabupaten Malinau", "Kabupaten Nunukan",
                    "Kabupaten Tana Tidung", "Kota Tarakan"
                ]
            },
            "Sulawesi Utara": {
                "ibukota": "Manado",
                "kabupaten_kota": [
                    "Kabupaten Bolaang Mongondow", "Kabupaten Bolaang Mongondow Selatan", "Kabupaten Bolaang Mongondow Timur",
                    "Kabupaten Bolaang Mongondow Utara", "Kabupaten Kepulauan Sangihe", "Kabupaten Kepulauan Siau Tagulandang Biaro",
                    "Kabupaten Kepulauan Talaud", "Kabupaten Minahasa", "Kabupaten Minahasa Selatan",
                    "Kabupaten Minahasa Tenggara", "Kabupaten Minahasa Utara", "Kota Bitung",
                    "Kota Kotamobagu", "Kota Manado", "Kota Tomohon"
                ]
            },
            "Gorontalo": {
                "ibukota": "Gorontalo",
                "kabupaten_kota": [
                    "Kabupaten Boalemo", "Kabupaten Bone Bolango", "Kabupaten Gorontalo",
                    "Kabupaten Gorontalo Utara", "Kabupaten Pohuwato", "Kota Gorontalo"
                ]
            },
            "Sulawesi Tengah": {
                "ibukota": "Palu",
                "kabupaten_kota": [
                    "Kabupaten Banggai", "Kabupaten Banggai Kepulauan", "Kabupaten Banggai Laut",
                    "Kabupaten Buol", "Kabupaten Donggala", "Kabupaten Morowali",
                    "Kabupaten Morowali Utara", "Kabupaten Parigi Moutong", "Kabupaten Poso",
                    "Kabupaten Sigi", "Kabupaten Tojo Una-Una", "Kabupaten Tolitoli",
                    "Kota Palu"
                ]
            },
            "Sulawesi Barat": {
                "ibukota": "Mamuju",
                "kabupaten_kota": [
                    "Kabupaten Majene", "Kabupaten Mamasa", "Kabupaten Mamuju",
                    "Kabupaten Mamuju Tengah", "Kabupaten Pasangkayu", "Kabupaten Polewali Mandar"
                ]
            },
            "Sulawesi Selatan": {
                "ibukota": "Makassar",
                "kabupaten_kota": [
                    "Kabupaten Bantaeng", "Kabupaten Barru", "Kabupaten Bone",
                    "Kabupaten Bulukumba", "Kabupaten Enrekang", "Kabupaten Gowa",
                    "Kabupaten Jeneponto", "Kabupaten Kepulauan Selayar", "Kabupaten Luwu",
                    "Kabupaten Luwu Timur", "Kabupaten Luwu Utara", "Kabupaten Maros",
                    "Kabupaten Pangkajene dan Kepulauan", "Kabupaten Pinrang", "Kabupaten Sidenreng Rappang",
                    "Kabupaten Sinjai", "Kabupaten Soppeng", "Kabupaten Takalar",
                    "Kabupaten Tana Toraja", "Kabupaten Toraja Utara", "Kabupaten Wajo",
                    "Kota Makassar", "Kota Palopo", "Kota Parepare"
                ]
            },
            "Sulawesi Tenggara": {
                "ibukota": "Kendari",
                "kabupaten_kota": [
                    "Kabupaten Bombana", "Kabupaten Buton", "Kabupaten Buton Selatan",
                    "Kabupaten Buton Tengah", "Kabupaten Buton Utara", "Kabupaten Kolaka",
                    "Kabupaten Kolaka Timur", "Kabupaten Kolaka Utara", "Kabupaten Konawe",
                    "Kabupaten Konawe Kepulauan", "Kabupaten Konawe Selatan", "Kabupaten Konawe Utara",
                    "Kabupaten Muna", "Kabupaten Muna Barat", "Kabupaten Wakatobi",
                    "Kota Baubau", "Kota Kendari"
                ]
            },
            "Maluku": {
                "ibukota": "Ambon",
                "kabupaten_kota": [
                    "Kabupaten Buru", "Kabupaten Buru Selatan", "Kabupaten Kepulauan Aru",
                    "Kabupaten Maluku Barat Daya", "Kabupaten Maluku Tengah", "Kabupaten Maluku Tenggara",
                    "Kabupaten Maluku Tenggara Barat", "Kabupaten Seram Bagian Barat", "Kabupaten Seram Bagian Timur",
                    "Kota Ambon", "Kota Tual"
                ]
            },
            "Maluku Utara": {
                "ibukota": "Sofifi",
                "kabupaten_kota": [
                    "Kabupaten Halmahera Barat", "Kabupaten Halmahera Tengah", "Kabupaten Halmahera Timur",
                    "Kabupaten Halmahera Selatan", "Kabupaten Halmahera Utara", "Kabupaten Kepulauan Sula",
                    "Kabupaten Pulau Morotai", "Kabupaten Pulau Taliabu", "Kota Ternate", "Kota Tidore Kepulauan"
                ]
            },
            "Papua": {
                "ibukota": "Jayapura",
                "kabupaten_kota": [
                    "Kabupaten Biak Numfor", "Kabupaten Jayapura", "Kabupaten Keerom",
                    "Kabupaten Kepulauan Yapen", "Kabupaten Mamberamo Raya", "Kabupaten Sarmi",
                    "Kabupaten Supiori", "Kabupaten Waropen", "Kota Jayapura"
                ]
            },
            "Papua Barat": {
                "ibukota": "Manokwari",
                "kabupaten_kota": [
                    "Kabupaten Fakfak", "Kabupaten Kaimana", "Kabupaten Manokwari",
                    "Kabupaten Manokwari Selatan", "Kabupaten Maybrat", "Kabupaten Pegunungan Arfak",
                    "Kabupaten Raja Ampat", "Kabupaten Sorong", "Kabupaten Sorong Selatan",
                    "Kabupaten Tambrauw", "Kabupaten Teluk Bintuni", "Kabupaten Teluk Wondama",
                    "Kota Sorong"
                ]
            },
            "Papua Selatan": {
                "ibukota": "Merauke",
                "kabupaten_kota": [
                    "Kabupaten Asmat", "Kabupaten Boven Digoel", "Kabupaten Mappi",
                    "Kabupaten Merauke", "Kabupaten Tabonji"
                ]
            },
            "Papua Tengah": {
                "ibukota": "Nabire",
                "kabupaten_kota": [
                    "Kabupaten Deiyai", "Kabupaten Dogiyai", "Kabupaten Intan Jaya",
                    "Kabupaten Mimika", "Kabupaten Nabire", "Kabupaten Paniai",
                    "Kabupaten Puncak", "Kabupaten Puncak Jaya"
                ]
            },
            "Papua Pegunungan": {
                "ibukota": "Jayawijaya",
                "kabupaten_kota": [
                    "Kabupaten Jayawijaya", "Kabupaten Lanny Jaya", "Kabupaten Mamberamo Tengah",
                    "Kabupaten Nduga", "Kabupaten Pegunungan Bintang", "Kabupaten Tolikara",
                    "Kabupaten Yalimo", "Kabupaten Yahukimo"
                ]
            }
        }

        self.api_key = "bd57384f99fd6d6d109c1c6469467468"
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

    def get_all_provinces(self):
        return sorted(self.provinces.keys())

    def get_regencies_by_province(self, province_name):
        if province_name in self.provinces:
            return sorted(self.provinces[province_name]["kabupaten_kota"])
        return []

    def get_all_regencies(self):
        all_regencies = []
        for province in self.provinces.values():
            all_regencies.extend(province["kabupaten_kota"])
        return sorted(all_regencies)

    def search_location(self, query):
        results = defaultdict(list)
        query = query.lower()
        for province in self.provinces:
            if query in province.lower():
                results["provinces"].append(province)
        for province, data in self.provinces.items():
            for regency in data["kabupaten_kota"]:
                if query in regency.lower():
                    results["regencies"].append((regency, province))
        return results

    def get_weather(self, location_name, use_api=False):
        search_results = self.search_location(location_name)
        if not search_results["provinces"] and not search_results["regencies"]:
            return {"error": "Location not found"}

        if use_api:
            params = {
                'q': location_name + ',ID',
                'appid': self.api_key,
                'units': 'metric'
            }
            try:
                response = requests.get(self.base_url, params=params)
                data = response.json()

                if response.status_code == 200:
                    return {
                        "location": location_name,
                        "temperature": f"{data['main']['temp']}°C",
                        "feels_like": f"{data['main']['feels_like']}°C",
                        "condition": data['weather'][0]['description'].title(),
                        "humidity": f"{data['main']['humidity']}%",
                        "wind_speed": f"{data['wind']['speed']} km/h",
                        "pressure": f"{data['main']['pressure']} hPa",
                        "visibility": f"{data['visibility'] / 1000} km",
                        "timestamp": datetime.fromtimestamp(data['dt']).strftime("%Y-%m-%d %H:%M:%S"),
                        "recommendation": self._get_recommendation(data['weather'][0]['main'])
                    }
                else:
                    return {"error": f"API Error: {data.get('message', 'Unknown error')}"}
            except Exception as e:
                return {"error": f"Failed to fetch data: {str(e)}"}
        else:
            condition_list = ["Clear", "Partly Cloudy", "Rain", "Thunderstorm", "Fog"]
            condition = condition_list[hash(location_name) % len(condition_list)]

            return {
                "location": location_name,
                "temperature": f"{25 + (hash(location_name) % 10)}°C",
                "feels_like": f"{24 + (hash(location_name) % 10)}°C",
                "condition": condition,
                "humidity": f"{40 + (hash(location_name) % 50)}%",
                "wind_speed": f"{5 + (hash(location_name) % 10)} km/h",
                "pressure": f"{1000 + (hash(location_name) % 20)} hPa",
                "visibility": f"{5 + (hash(location_name) % 15)} km",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "recommendation": self._get_recommendation(condition)
            }
    
    def get_weather_forecast(self, location_name, days=3, use_api=False):
        if use_api:
            params = {
                'q': location_name + ',ID',
                'appid': self.api_key,
                'units': 'metric'
            }
            try:
                response = requests.get(self.forecast_url, params=params)
                data = response.json()

                if response.status_code == 200:
                    forecast = []
                    for entry in data['list'][:days * 8:8]:
                        forecast.append({
                            "date": datetime.fromtimestamp(entry['dt']).strftime("%Y-%m-%d"),
                            "condition": entry['weather'][0]['description'].title(),
                            "min_temp": f"{entry['main']['temp_min']}°C",
                            "max_temp": f"{entry['main']['temp_max']}°C",
                            "humidity": f"{entry['main']['humidity']}%",
                            "wind_speed": f"{entry['wind']['speed']} km/h",
                            "recommendation": self._get_recommendation(entry['weather'][0]['main'])
                        })
                    return forecast
                else:
                    return [{"error": f"API Error: {data.get('message', 'Unknown error')}"}]
            except Exception as e:
                return [{"error": f"Failed to fetch forecast: {str(e)}"}]
        else:
            forecast = []
            for day in range(days):
                condition_list = ["Clear", "Partly Cloudy", "Rain", "Thunderstorm"]
                condition = condition_list[hash(location_name + str(day)) % len(condition_list)]
                forecast.append({
                    "date": (datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d"),
                    "condition": condition,
                    "min_temp": f"{24 + (hash(location_name + str(day)) % 5)}°C",
                    "max_temp": f"{30 + (hash(location_name + str(day)) % 6)}°C",
                    "humidity": f"{50 + (hash(location_name + str(day)) % 40)}%",
                    "wind_speed": f"{5 + (hash(location_name + str(day)) % 15)} km/h",
                    "recommendation": self._get_recommendation(condition)
                })
            return forecast

    def _get_recommendation(self, condition):
        recommendations = {
            "Clear": "Wear sunscreen and stay hydrated.",
            "Partly Cloudy": "Carry an umbrella just in case.",
            "Rain": "Use a raincoat or umbrella.",
            "Thunderstorm": "Avoid outdoor activities.",
            "Fog": "Drive carefully due to low visibility."
        }
        return recommendations.get(condition, "No specific recommendation.")


def display_table(data, columns=3, max_width=30):
    for i in range(0, len(data), columns):
        row = data[i:i+columns]
        print(" | ".join(f"{item:<{max_width}}" for item in row))

def main():
    analyzer = WeatherAnalyzerIndonesia()

    print("\n=== INDONESIA WEATHER ANALYZER By @ThurZ ===")
    print(f"● Total Provinces: {len(analyzer.get_all_provinces())}")
    print(f"● Total Regencies/Cities: {len(analyzer.get_all_regencies())}")

    while True:
        print("\n🔹 MAIN MENU:")
        print("1. List All Provinces")
        print("2. List Regencies/Cities in a Province")
        print("3. Search for a Location")
        print("4. Check Current Weather")
        print("5. Get 3-Day Weather Forecast")
        print("6. List All Regencies & Cities")
        print("7. Exit")

        choice = input("\nChoose an option (1-7): ").strip()

        if choice == "1":
            print("\n📌 List of All Provinces in Indonesia:")
            provinces = analyzer.get_all_provinces()
            display_table(provinces, columns=4)

        elif choice == "2":
            province = input("\nEnter province name: ").strip()
            regencies = analyzer.get_regencies_by_province(province)
            if regencies:
                print(f"\n📋 Regencies & Cities in {province}:")
                display_table(regencies, columns=3)
                print(f"\nTotal: {len(regencies)} regencies/cities")
            else:
                print("⚠️ Province not found. Try again.")

        elif choice == "3":
            query = input("\n🔍 Enter location name to search: ").strip()
            results = analyzer.search_location(query)
            if results["provinces"] or results["regencies"]:
                if results["provinces"]:
                    print("\n✅ Matching Provinces:")
                    for province in results["provinces"]:
                        print(f"- {province}")
                if results["regencies"]:
                    print("\n✅ Matching Regencies/Cities:")
                    for regency, province in results["regencies"]:
                        print(f"- {regency} ({province})")
            else:
                print("⚠️ No matching locations found.")

        elif choice == "4":
            location = input("\n🌤️ Enter location (province/regency/city): ").strip()
            weather = analyzer.get_weather(location)
            if "error" in weather:
                print(f"\n❌ Error: {weather['error']}")
            else:
                print("\n📊 Current Weather Report:")
                for key, value in weather.items():
                    print(f"• {key.replace('_', ' ').title()}: {value}")

        elif choice == "5":
            location = input("\n🌦️ Enter location for forecast: ").strip()
            forecast = analyzer.get_weather_forecast(location, days=3)
            if "error" in forecast[0]:
                print(f"\n❌ Error: {forecast[0]['error']}")
            else:
                print(f"\n📅 3-Day Weather Forecast for {location}:")
                for day in forecast:
                    print(f"\n📌 Date: {day['date']}")
                    print(f"☁️ Condition: {day['condition']}")
                    print(f"🌡️ Temperature: {day['min_temp']} to {day['max_temp']}")
                    print(f"💧 Humidity: {day['humidity']}")
                    print(f"🌬️ Wind Speed: {day['wind_speed']}")
                    print(f"💡 Recommendation: {day['recommendation']}")

        elif choice == "6":
            print("\n📜 All Regencies & Cities in Indonesia:")
            all_regencies = analyzer.get_all_regencies()
            display_table(all_regencies, columns=3)
            print(f"\nTotal: {len(all_regencies)} regencies/cities")

        elif choice == "7":
            print("\n👋 Thank you for using Indonesia Weather Analyzer!")
            break

        else:
            print("\n⚠️ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()