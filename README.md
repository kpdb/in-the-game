# InTheGame

Projekt z serii "niedokończonych opowieści". Wymaga jeszcze sporo pracy aby stać się użyteczną aplikacją, ale pokazuje ogólny i w niektórych miejscach działający zarys całości.

## Podstawowa architektura

Aplikację bardzo dobrze nadaje się do implementacji w stylu serverless, ale w ramach tego zadania postanowiłem wykonać ją w sposób "chmuroniezależny". Składa się z czterech podstawowych komponentów:
- API: implementując serię końcówek w standardzie REST umożliwia użytkownikom dostęp do danych o drużynach i spotkaniach, które między sobą odbywają
- Baza danych SQL: pozwala przechowywać dane serwowane potem przy pomocy API
- Worker: aplikacja działająca w tle i realizująca zadania, które nie wymagają bezpośredniej interakcji z użytkownikiem
- Kolejka wiadomości: usługa pozwalająca na asynchroniczne zlecanie realizacji zadań realizowanych przez Worker

### API

Aplikacja świadcząca funkcję REST API została zaimplementowana w Pythonie, przy pomocy frameworku FastAPI. Jest to stosunkowo młode rozwiązanie, ale wypadające bardzo korzystnie w benchmarkach wydajności. Dodatkowo, powstał z myślą o implementacji API i w związku z tym udostępnia kilka narzędzi bardzo uprzyjemniających pracę: wbudowaną stronę dokumentację OpenAPI dostępną w aplikacji pod `/docs` prezentowaną na podstawie automatycznie generowanej schemy OpenAPI. Schema jest generowana na podstawie końcówek zaimplementowanych przez programistę i podpiętych do obiektu aplikacji oraz modelu danych zaimplementowanego przy pomocy klas pochodzących z biblioteki `pydantic`. Całość, pozwala na bardzo intuicyjną pracę, szczególnie, że API frameworku FastAPI jest bardzo podobne do tego, z którym można spotkać się w Flasku.

### Worker

Zadania realizowane w ramach workera uruchamiane są przez mechanizmy biblioteki `arq`. Pozwala ona w łatwy sposób zaimplementować kolejkę zadań dając duży zapas możliwości takich jak:
- prosty cronowy scheduler,
- zlecanie zadań z zadanym opóźnieniem,
- ponawianie i anulowanie zadań,
- zapewnienie unikalności zadań - zadanie o takich samych cechach nie zostanie zakolejkowane dopóki nie zakończy się już to istniejące w systemie.

Wybrałem go jednak głównie z uwagi na możliwość pisania zadań przy pomocy korutyn, a to pozwala na łatwe napisanie "asynchronicznego" kodu, który będzie współdzielony z API. Korutyny nie są w żaden sposób udekorowane, a `arq` wstrzykuje jedynie do ich wnętrza obiekt kontekstu, który musi być zadeklarowany jako pierwszy z argumentów korutyny - upraszcza to choćby pisanie testów jednostkowych.

Należy jednak wspomnieć, że jest on bardzo mocno zintegrowany z Redis, który pełni w tym przypadku rolę kolejki wiadomości. Zazwyczaj Redis i tak jest wykorzystywany w wielu projektach (choćby jako cache server), ale jeśli konieczne jest użycie innego brokera, lepiej wybrać `Celery`.

### Baza danych SQL

Przyznam, że na bazę danych wybrałem PostgreSQL, głównie z przyzwyczajenia. W pythonie ma dobre wsparcie dla `asyncio`, co dawało mi gwarancję bezproblemowego działania w projekcie na poziomie sterownika bazy danych.

### Kolejka wiadomości

Ten wybór został podyktowany wybraniem biblioteki `arq` przy implementacji workera - nie rozmawia ona z niczym innym niż Redis. Projekt nie jest jednak pokrzywdzony z tego powodu, bo jest to na tyle uniwersalne narzędzie, że z powodzeniem może zostać wykorzystane cache-server, czy wsparcie mechanizmu powiadamiania "na żywo" z wykorzystaniem redisowego mechanizmu PubSub.

## Pozostała dokumentacja

W ramach opisu projektu w katalogu `docs` repozytorium umieściłem diagramy UML (i definicje PlantUML, z których zostały wygenerowane):
- diagram klas; dość symbolicznie pokazujący zarys całego systemu
- diagramy aktywności przedstawiające ideę wysyłania powiadomień: osobno "weekly", "daily" i "live".

Model danych opisałem przy pomocy języka DBML i wygenerowałem z niego plik graficzny.
Definicja API została dołączona w pliku `openapi.json` wygenerowanym przez FastAPI.

## Uruchamianie

Na potrzeby developerskiego uruchomienia komponentów aplikacji przygotowałem plik `docker-compose.yml`.

Zbudowane obrazu aplikacji, pobranie obrazów baz danych i uruchomienie całości:
```
docker-compose up -d --build
```

Utworzenie schematu bazy danych:
```
docker-compose exec api poetry run alembic upgrade head
```

API dostępne jest na maszynie lokalnej, na porcie 8002. A pod adresem `http://localhost:8002/docs` można zobaczyć jego dokumentację.
