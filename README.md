
GENERATOR GRAFIKU --- Mikołaj Szyra

To jest część kodu, która na gotowych danych (przetworzonych przez program dataconverter.py) układa możliwie jak najlepszy grafik dla danych
uczniów, korepetytorów, sal oraz ich wszystkich dostępności.


Celem tego programu jest zaoszczedzenie czasu osobie odpowiedzialnej za ręczne ułożenie grafiku. Bazujemy na prawdziwych, zanonimizowanych danych wyciągnietych z systemu firmy.
Dlatego potrzebny jest etap konwertowania tych danych na takie, na których można łatwo działać.

Plik LESSONSYSTEM_DATA_INPUT.json zawiera :
 intentions - zgłoszenia : Dany uczeń, chce lekcje z takim nauczycielem (uczącym wyganaego przedmoitu), w ilosci takiej
resources - zawiera dostępności uczniów, nauczycieli i sal.

Algorytm nie dązy do idealnego, optymalnego ułozenia dlatego, że jest to nieosiągalne. Chodzi o to, aby stworzyć dobrą bazę, na której można wprowadzać poprawki. 

Pierwsze działanie programu było prostą pętlą po kolei iterującą najpierw po intentions ( ponizej zamieszczam przykład). Dla każdego po kolei szukało terminu
w następujacym schemacie :

*Iteracja po dostępnych nauczycielach
    *dla każdego, w danym dniu, próbował znależć pasujący wolny termin z uczniem (zapisanym w intentions) po godzinach wypisanych w dostepnosciach danego dnia 
     zawartych w resources.  
        *Ostatecznie dobierał im salę do wyznaczonej godziny. 

Gdy to działało zacząłem ulepszac rozwiązanie np wprowadzając:

*losowanie dnia, tak aby nie zaczynał zawsze od poniedziałku.
*wprowadzenie funkcji "ocena_atrakcyjnosci" aby faworyzował godziny w blokach, aby nauczyciele nie mieli okienek. Funkcja ta przyznaje punkty
 godzinie za bycie "sasiadem" godziny z tagiem "ZAJETE'. Nastepie  dzieki tej funkcji układamy godziny malejąco w rankingu punktów. 
* Uwzględnienie preferowanej sali przez ucznia poprzez umieszczenie jej jako pierwszą na liscie sal w danej iteracji.

Gdy zacząłem pracować nad faworyzacją wczesnych godzin uczniów (żeby wybierał do przydzielenia najpierw uczniów z dostępnymi godzinami porannymi, bo jest na nich mniejsze obłozenie)
system nie notował progresu. Zatrzymałem się na 263 godzinach dla całej grupy. Nawet czasem notował spadki. Pomyślałem wtedy, że jedyne co optymalizuje to kolejność iterowania po intentions.
Doszedłem do wniosku, że najskuteczniejsze jest wykoanie wielu losowych ustawien, im więcej tym lepiej. Wtedy nie muszę przewidywać wielu problemów i próbować je rozwiązywać 
tylko wybierać ze skonczonej możliwości kombinacji te najskuteczniejszą, którą uda się odkryć. Więc zająłem się funkcją "main" aby wykonywała np.100,1000 prób i w każdej losowała 
kolejność intentions, a następnie dla niej wywoływała funkcję generującą grafik "generate_schedule". Wtedy zacząłem notowac wzrost do nawet 269 godzin. Może nie brzmiec to 
oszałamiająco, jednak udalo sie znaleźć rozwiązania tylko za pomocą mieszania kolejności wywołań !

* To było ostatnie udoskonalenie programu.

Liczba możliwych przydziałów godzin dla takiej grupy jest skończona. Możliwe, że dla dziesiątek czy setektysięcy wywołań (przeprowadziłem próbę dla 10000, wynikiem było 269)
liczba ta wcale może nie wzrosnąc drastycznie. Co świadczy o naszym satysfakconującym wyniku.

W funkcji "main" również znajduje się reprezentacja danych w rich oraz pokazywanie progressu procesu w czasie rzeczywistym w tqdm.


 {
            "id": 217,
            "student_id": 201,
            "subject_id": 1003,
            "weekly_sessions": 2,
            "possible_tutors_ids": [
                1,
                9,
                10,
                14,
                18,
                19,
                27,
                32,
                34,
                35,
                38,
                39
            ],
            "preferred_location_id": 2,
            "notes": ""
        },
