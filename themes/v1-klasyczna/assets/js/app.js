/* ==========================================================================
   Szablon demo V1 - caly JavaScript serwisu.

   Zasady:
   - zero bibliotek: oryginal ladowal jQuery 1.4 z 2010 r. z obcego serwera
     (plus zapasowa kopia lokalna, ktora zwracala HTTP 404) i fancybox 1.3.4;
     tutaj nie ma ani jednego zapytania na zewnatrz
   - plik jest ladowany z atrybutem defer, wiec nie blokuje renderowania
   - kazda funkcja sprawdza, czy jej element w ogole jest na stronie; bez JS
     strona dziala dalej, traci tylko udogodnienia
   ========================================================================== */
(function () {
  "use strict";

  var $  = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };

  /* Napisy przychodza z szablonu w atrybutach data-napis-<nazwa> (teksty
     w i18n/pl.yaml motywu), wiec w tym pliku nie ma tekstow strony.
     {klucz} w napisie zastepuje wartosc z "wartosci". */
  var napis = function (el, nazwa, wartosci) {
    return (el.getAttribute("data-napis-" + nazwa) || "").replace(/\{(\w+)\}/g, function (cale, klucz) {
      return wartosci && klucz in wartosci ? String(wartosci[klucz]) : cale;
    });
  };

  /* ------------------------------------------------------------ 1. Motyw */
  /* Wybor uzytkownika wygrywa z ustawieniem systemu i przezywa przeladowanie.
     Skrypt ustawiajacy atrybut data-theme siedzi w <head> kazdej podstrony,
     zeby strona nie mrugnela jasnym tlem przed wczytaniem tego pliku.
     Przycisk ma stala etykiete ("Ciemny motyw"), a stan podaje aria-pressed -
     ustawiane od razu po wczytaniu, po kliknieciu i po zmianie motywu systemu. */

  var root = document.documentElement;
  var systemDark = window.matchMedia("(prefers-color-scheme: dark)");
  var themeToggles = $$("[data-theme-toggle]");
  var isDark = function () {
    var theme = root.getAttribute("data-theme");
    return theme ? theme === "dark" : systemDark.matches;
  };
  var syncThemeToggles = function () {
    var pressed = String(isDark());
    themeToggles.forEach(function (btn) { btn.setAttribute("aria-pressed", pressed); });
  };

  themeToggles.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var next = isDark() ? "light" : "dark";
      root.setAttribute("data-theme", next);
      syncThemeToggles();
      try { localStorage.setItem("motyw", next); } catch (e) { /* tryb prywatny */ }
    });
  });
  syncThemeToggles();
  if (systemDark.addEventListener) systemDark.addEventListener("change", syncThemeToggles);

  /* --------------------------------------------------- 2. Menu na telefonie */

  var drawer = $("#menu-mobilne");
  var navToggle = $("[data-nav-toggle]");

  if (drawer && navToggle) {
    var lastFocused = null;

    var openDrawer = function () {
      lastFocused = document.activeElement;
      drawer.setAttribute("data-open", "true");
      drawer.removeAttribute("inert");
      navToggle.setAttribute("aria-expanded", "true");
      document.body.style.overflow = "hidden";
      var first = $("a, button", drawer);
      if (first) first.focus();
    };

    var closeDrawer = function () {
      drawer.setAttribute("data-open", "false");
      drawer.setAttribute("inert", "");
      navToggle.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
      if (lastFocused) lastFocused.focus();
    };

    drawer.setAttribute("inert", "");
    navToggle.addEventListener("click", function () {
      drawer.getAttribute("data-open") === "true" ? closeDrawer() : openDrawer();
    });
    $$("[data-drawer-close]", drawer).forEach(function (el) {
      el.addEventListener("click", closeDrawer);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && drawer.getAttribute("data-open") === "true") closeDrawer();
    });
  }

  /* Podmenu "Usługi" w pasku na duzym ekranie - obsluga klawiatury */
  $$("[data-submenu-toggle]").forEach(function (btn) {
    var wrap = btn.closest(".nav__has-sub");
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!open));
    });
    document.addEventListener("click", function (e) {
      if (wrap && !wrap.contains(e.target)) btn.setAttribute("aria-expanded", "false");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") btn.setAttribute("aria-expanded", "false");
    });
  });

  /* ----------------------------------------------------- 3. "Otwarte teraz" */
  /* Godziny przyjec sa zapisane w atrybucie data-godziny na elemencie
     [data-status], w formacie "1:9:00-17:00;2:9:00-17:00;..." gdzie
     1 = poniedzialek. Dzieki temu jest JEDNO zrodlo prawdy dla banera,
     tabeli godzin i danych strukturalnych openingHours. */

  $$("[data-status]").forEach(function (el) {
    var raw = el.getAttribute("data-godziny") || "";
    // Pusto znaczy "godziny niepotwierdzone" - zostawiamy zapasowy napis
    // z layoutu, zamiast zgadywac stan gabinetu.
    if (!raw) return;
    var map = {};
    raw.split(";").forEach(function (part) {
      var bits = part.split(":");
      if (bits.length < 2) return;
      map[Number(bits[0])] = part.slice(part.indexOf(":") + 1);
    });

    var now = new Date();
    var day = now.getDay() === 0 ? 7 : now.getDay();
    var minutes = now.getHours() * 60 + now.getMinutes();
    var today = map[day];
    var open = false;
    var toMin = function (hhmm) {
      var p = hhmm.trim().split(":");
      return Number(p[0]) * 60 + Number(p[1] || 0);
    };

    if (today) {
      var se = today.split("-");
      open = minutes >= toMin(se[0]) && minutes < toMin(se[1]);
    }

    el.classList.add(open ? "is-open" : "is-closed");
    var label = $("[data-status-label]", el);
    if (!label) return;

    if (open) {
      label.textContent = napis(el, "otwarte", { godzina: map[day].split("-")[1] });
    } else {
      /* Najblizszy dzien przyjec, liczac od jutra, maksymalnie tydzien w przod.
         Przyimek siedzi w napisie razem z nazwa dnia (data-napis-dni), bo po
         polsku jest "we wtorek", a nie "w wtorek". */
      var names = [""].concat((el.getAttribute("data-napis-dni") || "").split("|"));
      var nextDay = null;
      if (today && minutes < toMin(today.split("-")[0])) {
        label.textContent = napis(el, "dzis", { godzina: map[day].split("-")[0] });
        return;
      }
      for (var i = 1; i <= 7; i++) {
        var d = ((day - 1 + i) % 7) + 1;
        if (map[d]) { nextDay = d; break; }
      }
      label.textContent = nextDay
        ? napis(el, "otwieramy", { dzien: names[nextDay] || "", godzina: map[nextDay].split("-")[0] })
        : napis(el, "zamkniete");
    }
  });

  /* Podswietlenie dzisiejszego wiersza w tabeli godzin */
  $$(".hours [data-dzien='" + (new Date().getDay() === 0 ? 7 : new Date().getDay()) + "']").forEach(function (row) {
    row.setAttribute("data-today", "");
  });

  /* -------------------------------------------------------- 4. Powiekszanie */
  /* Zastepuje fancybox 1.3.4 + jQuery 1.4 (razem ok. 95 kB) natywnym
     elementem <dialog>. Koszt: 0 kB pobierania. */

  var lightbox = $("#lightbox");
  if (lightbox) {
    var lbImg = $("[data-lb-img]", lightbox);
    var lbCap = $("[data-lb-cap]", lightbox);
    var items = $$("[data-lightbox]");
    var index = 0;

    var show = function (i) {
      index = (i + items.length) % items.length;
      var btn = items[index];
      lbImg.src = btn.getAttribute("data-full");
      lbImg.alt = btn.getAttribute("data-alt") || "";
      lbCap.textContent = (btn.getAttribute("data-alt") || "") + "  " +
        napis(lightbox, "licznik", { nr: index + 1, razem: items.length });
    };

    items.forEach(function (btn, i) {
      btn.addEventListener("click", function () {
        show(i);
        if (typeof lightbox.showModal === "function") lightbox.showModal();
      });
    });

    $$("[data-lb-prev]", lightbox).forEach(function (b) {
      b.addEventListener("click", function () { show(index - 1); });
    });
    $$("[data-lb-next]", lightbox).forEach(function (b) {
      b.addEventListener("click", function () { show(index + 1); });
    });
    $$("[data-lb-close]", lightbox).forEach(function (b) {
      b.addEventListener("click", function () { lightbox.close(); });
    });

    lightbox.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); show(index + 1); }
      if (e.key === "ArrowLeft")  { e.preventDefault(); show(index - 1); }
    });

    /* Klikniecie w tlo zamyka okno */
    lightbox.addEventListener("click", function (e) {
      if (e.target === lightbox) lightbox.close();
    });
  }

  /* ------------------------------------------------------------- 5. Mapa */
  /* Mapa Google jest doladowywana dopiero po swiadomym klknieciu.
     Powod jest prawny, nie wydajnosciowy: osadzona ramka wysyla adres IP
     pacjenta do Google jeszcze zanim ktokolwiek o cokolwiek zapytal.
     Przy okazji strona kontaktu schudla o 1-2 MB. */

  /* Tytul ramki (czytany przez czytnik ekranu) bierze adres z parametru q
     adresu mapy. Ten adres szablon sklada z data/gabinet.yaml, wiec po
     zmianie adresu w CMS tytul zmienia sie razem z mapa - zamiast trzymac
     tutaj druga, zapomniana kopie adresu. Poczatek tytulu: data-napis-tytul. */
  var tytulMapy = function (box, src) {
    var adres = "";
    try { adres = new URL(src, location.href).searchParams.get("q") || ""; } catch (e) { /* stara przegladarka */ }
    return napis(box, "tytul") + (adres ? ": " + adres : "");
  };

  $$("[data-map]").forEach(function (box) {
    var btn = $("[data-map-load]", box);
    if (!btn) return;
    btn.addEventListener("click", function () {
      var frame = document.createElement("iframe");
      frame.src = box.getAttribute("data-map-src");
      frame.title = tytulMapy(box, frame.src);
      frame.loading = "lazy";
      frame.referrerPolicy = "no-referrer-when-downgrade";
      frame.setAttribute("allowfullscreen", "");
      box.innerHTML = "";
      box.appendChild(frame);
      try { sessionStorage.setItem("mapa-zgoda", "1"); } catch (e) { /* tryb prywatny */ }
    });
    try {
      if (sessionStorage.getItem("mapa-zgoda") === "1") btn.click();
    } catch (e) { /* tryb prywatny */ }
  });

  /* ------------------------------------------------------ 6. Filtr cennika */

  var priceSearch = $("[data-price-search]");
  if (priceSearch) {
    var table = $("#cennik-tabela");
    var counter = $("[data-price-count]");
    var rows = $$("tbody tr:not(.group)", table);
    var groups = $$("tbody tr.group", table);

    var filter = function () {
      var q = priceSearch.value.trim().toLowerCase();
      var shown = 0;
      rows.forEach(function (tr) {
        var hit = !q || tr.textContent.toLowerCase().indexOf(q) > -1;
        tr.hidden = !hit;
        if (hit) shown++;
      });
      /* Naglowek grupy znika, jesli w grupie nie zostal ani jeden wiersz */
      groups.forEach(function (g) {
        var any = false;
        var tr = g.nextElementSibling;
        while (tr && !tr.classList.contains("group")) {
          if (!tr.hidden) { any = true; break; }
          tr = tr.nextElementSibling;
        }
        g.hidden = !any;
      });
      if (counter) {
        counter.textContent = q
          ? napis(counter, "pasujace", { liczba: shown })
          : napis(counter, "wszystkie", { liczba: rows.length });
      }
    };

    priceSearch.addEventListener("input", filter);
    filter();
  }

  /* ---------------------------------------------- 7. Formularz kontaktowy */
  /* Formularz jeszcze niczego nie wysyla (brak obslugi na serwerze). Tu
     pokazujemy wylacznie zachowanie interfejsu i komplet pol wymaganych przez
     RODO. Kazdy formularz na stronie osobno; komunikat stoi zaraz po nim. */

  $$("[data-demo-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var box = form.nextElementSibling;
      if (box && box.hasAttribute("data-form-result")) {
        box.hidden = false;
        box.focus();
        box.scrollIntoView({ block: "center", behavior: "smooth" });
      }
      form.hidden = true;
    });
  });

  /* -------------------------------------------------- 8. Rok w stopce */

  $$("[data-rok]").forEach(function (el) { el.textContent = String(new Date().getFullYear()); });

  /* --------------------------------------------- 9. Animacje wejscia */
  /* Bloki sekcji (main .section) pojawiaja sie przy pierwszym wejsciu w widok:
     z dolu, kolumny tekstu ze zdjeciem z lewej i z prawej, karty i kroki po
     kolei (opoznienie liczone z tego, co wchodzi w widok naraz - na telefonie
     karta w jednej kolumnie nie czeka na poprzednie). Klase "ruch" na <html>
     ustawia skrypt w head.html (tylko gdy przegladarka ma IntersectionObserver
     i nie ma "ogranicz ruch"); bez niej nic nie jest ukryte. Baner i naglowek podstrony nie sa animowane (LCP).
     To, co jest w widoku przy wejsciu na strone, pokazuje sie od razu - bez
     mrugniecia. Fokus klawiatury, kotwica w adresie i druk odslaniaja tresc. */

  var html = document.documentElement;
  if (html.classList.contains("ruch")) {
    var cele = [];
    var oznacz = function (el, kierunek) {
      el.setAttribute("data-ruch", kierunek);
      cele.push(el);
    };
    var kolejno = function (lista, kierunek) {
      lista.forEach(function (el) { oznacz(el, kierunek); });
    };
    var przejdz = function (kontener) {
      Array.prototype.slice.call(kontener.children).forEach(function (el) {
        var c = el.classList;
        if (el.tagName === "DIALOG" || el.tagName === "SCRIPT" || c.contains("visually-hidden")) return;
        if (c.contains("blok-dalej")) { przejdz(el); return; }
        if (c.contains("split")) {
          var kol = Array.prototype.slice.call(el.children);
          if (kol[0]) oznacz(kol[0], "lewo");
          if (kol[1]) oznacz(kol[1], "prawo");
        } else if (c.contains("grid") || c.contains("trust") || c.contains("related")) {
          kolejno(Array.prototype.slice.call(el.children), "gora");
        } else if (c.contains("gallery")) {
          kolejno(Array.prototype.slice.call(el.children), "skala");
        } else if (c.contains("steps")) {
          kolejno($$(":scope > li", el), "lewo");
        } else if (c.contains("faq")) {
          kolejno($$(":scope > details", el), "gora");
        } else if (c.contains("table-wrap") || c.contains("map-embed") || el.tagName === "FORM") {
          oznacz(el, "pojaw");
        } else {
          oznacz(el, "gora");   /* naglowek, wstep, tekst, ramka */
        }
      });
    };
    $$("main .section > .container").forEach(przejdz);

    /* po wjezdzie element wraca do zwyklych przejsc (np. uniesienie karty
       pod kursorem) - bez znacznikow animacji i opoznienia */
    var sprzataj = function (el) {
      el.removeAttribute("data-ruch");
      el.removeAttribute("data-ruch-widoczny");
      el.style.removeProperty("--ruch-opoznienie");
    };
    var pokaz = function (el) {
      if (!el.hasAttribute("data-ruch") || el.hasAttribute("data-ruch-widoczny")) return;
      el.setAttribute("data-ruch-widoczny", "");
      var raz = function (e) {
        if (e && e.target !== el) return;   /* przejscia elementow w srodku */
        el.removeEventListener("transitionend", raz);
        sprzataj(el);
      };
      el.addEventListener("transitionend", raz);
      setTimeout(raz, 1600);   /* gdy transitionend nie przyjdzie (np. element ukryty) */
    };
    var wysokosc = window.innerHeight || html.clientHeight;
    var obserwator = new IntersectionObserver(function (wpisy) {
      /* co wchodzi naraz, wjezdza po kolei (w kolejnosci dokumentu), co 80 ms,
         najwyzej 6 krokow */
      wpisy.filter(function (w) { return w.isIntersecting; })
        .map(function (w) { return w.target; })
        .sort(function (a, b) { return a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1; })
        .forEach(function (el, i) {
          el.style.setProperty("--ruch-opoznienie", (Math.min(i, 6) * 0.08).toFixed(2) + "s");
          pokaz(el);
          obserwator.unobserve(el);
        });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });

    cele.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < wysokosc && r.bottom > 0) {
        /* w widoku od poczatku: bez animacji, zeby nic nie zniknelo na chwile */
        el.style.transition = "none";
        pokaz(el);
        requestAnimationFrame(function () { el.style.transition = ""; });
      } else {
        obserwator.observe(el);
      }
    });

    /* odslania cel i wszystko, co stoi przed nim w dokumencie (kotwica, fokus) */
    var odslonDo = function (cel) {
      if (!cel) return;
      cele.forEach(function (el) {
        if (el === cel || el.contains(cel) || cel.contains(el) ||
            (el.compareDocumentPosition(cel) & Node.DOCUMENT_POSITION_FOLLOWING)) {
          pokaz(el); obserwator.unobserve(el);
        }
      });
    };
    var zKotwicy = function () {
      var id = decodeURIComponent((location.hash || "").slice(1));
      if (id) odslonDo(document.getElementById(id));
    };
    zKotwicy();
    window.addEventListener("hashchange", zKotwicy);
    document.addEventListener("focusin", function (e) {
      var el = e.target.closest && e.target.closest("[data-ruch]:not([data-ruch-widoczny])");
      if (el) odslonDo(el);
    });
    window.addEventListener("beforeprint", function () { cele.forEach(pokaz); });

    html.classList.add("ruch-gotowy");
  }
})();
