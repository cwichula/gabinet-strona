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

  /* ------------------------------------------------------------ 1. Motyw */
  /* Wybor uzytkownika wygrywa z ustawieniem systemu i przezywa przeladowanie.
     Skrypt ustawiajacy atrybut data-theme siedzi w <head> kazdej podstrony,
     zeby strona nie mrugnela jasnym tlem przed wczytaniem tego pliku. */

  $$("[data-theme-toggle]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var root = document.documentElement;
      var dark = root.getAttribute("data-theme")
        ? root.getAttribute("data-theme") === "dark"
        : window.matchMedia("(prefers-color-scheme: dark)").matches;
      var next = dark ? "light" : "dark";
      root.setAttribute("data-theme", next);
      btn.setAttribute("aria-label", next === "dark" ? "Włącz jasny motyw" : "Włącz ciemny motyw");
      try { localStorage.setItem("motyw", next); } catch (e) { /* tryb prywatny */ }
    });
  });

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
      label.textContent = "Otwarte teraz · do " + map[day].split("-")[1];
    } else {
      /* Najblizszy dzien przyjec, liczac od jutra, maksymalnie tydzien w przod.
         Przyimek siedzi w tablicy razem z nazwa dnia, bo po polsku jest
         "we wtorek", a nie "w wtorek". */
      var names = ["", "w poniedziałek", "we wtorek", "w środę", "w czwartek",
                   "w piątek", "w sobotę", "w niedzielę"];
      var nextDay = null;
      if (today && minutes < toMin(today.split("-")[0])) {
        label.textContent = "Dziś od " + map[day].split("-")[0];
        return;
      }
      for (var i = 1; i <= 7; i++) {
        var d = ((day - 1 + i) % 7) + 1;
        if (map[d]) { nextDay = d; break; }
      }
      label.textContent = nextDay
        ? "Zamknięte · otwieramy " + names[nextDay] + " o " + map[nextDay].split("-")[0]
        : "Zamknięte";
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
      lbCap.textContent = (btn.getAttribute("data-alt") || "") +
        "  (" + (index + 1) + " z " + items.length + ")";
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
     tutaj druga, zapomniana kopie adresu. */
  var tytulMapy = function (src) {
    var adres = "";
    try { adres = new URL(src, location.href).searchParams.get("q") || ""; } catch (e) { /* stara przegladarka */ }
    return "Mapa dojazdu do gabinetu" + (adres ? ": " + adres : "");
  };

  $$("[data-map]").forEach(function (box) {
    var btn = $("[data-map-load]", box);
    if (!btn) return;
    btn.addEventListener("click", function () {
      var frame = document.createElement("iframe");
      frame.src = box.getAttribute("data-map-src");
      frame.title = tytulMapy(frame.src);
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
          ? "Pasujące pozycje: " + shown
          : "Wszystkich pozycji w cenniku: " + rows.length;
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
})();
