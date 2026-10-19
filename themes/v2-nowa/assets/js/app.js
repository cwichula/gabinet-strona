/* ==========================================================================
   v2-nowa - caly JavaScript serwisu (bez bibliotek, bez zapytan na zewnatrz).

   Zasady (jak v1-klasyczna):
   - plik ladowany z defer, nie blokuje renderowania;
   - kazda funkcja sprawdza, czy jej element jest na stronie; bez JS strona
     dziala dalej (tresc widoczna, tabela godzin, pelny cennik), traci tylko
     udogodnienia;
   - napisy przychodza z szablonu w atrybutach data-napis-* (i18n/pl.yaml
     motywu), wiec w tym pliku nie ma tekstow strony.
   ========================================================================== */
(function () {
  "use strict";

  var $  = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };
  var root = document.documentElement;
  var ruch = !window.matchMedia || !matchMedia("(prefers-reduced-motion: reduce)").matches;

  var napis = function (el, nazwa, wartosci) {
    return (el.getAttribute("data-napis-" + nazwa) || "").replace(/\{(\w+)\}/g, function (cale, klucz) {
      return wartosci && klucz in wartosci ? String(wartosci[klucz]) : cale;
    });
  };

  /* ------------------------------------------------------------ 1. Motyw */
  /* Wybor uzytkownika wygrywa z ustawieniem systemu i przezywa przeladowanie
     (skrypt w <head> ustawia data-theme przed pierwszym malowaniem).
     Przycisk ma stala etykiete ("Ciemny motyw"), stan podaje aria-pressed. */
  var systemDark = window.matchMedia ? matchMedia("(prefers-color-scheme: dark)") : { matches: false };
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

  /* ---------------------------------------------- 2. Szuflada i podmenu */
  var drawer = $("#menu-mobilne");
  var navToggle = $("[data-nav-toggle]");
  if (drawer && navToggle) {
    var lastFocused = null;
    var focusable = function () {
      return $$("a[href], button:not([disabled]), summary, input, [tabindex]", drawer)
        .filter(function (el) { return el.offsetParent !== null && el.getAttribute("tabindex") !== "-1"; });
    };
    /* reszta strony nieaktywna, gdy szuflada jest otwarta (czytnik w trybie
       przegladania nie wychodzi poza okno) */
    var tlo = $$("body > *").filter(function (el) {
      return el !== drawer && !el.contains(drawer) && el.tagName !== "SCRIPT";
    });
    var zablokujTlo = function (tak) {
      tlo.forEach(function (el) { if (tak) el.setAttribute("inert", ""); else el.removeAttribute("inert"); });
    };
    var openDrawer = function () {
      lastFocused = document.activeElement;
      drawer.setAttribute("data-open", "true");
      drawer.removeAttribute("inert");
      navToggle.setAttribute("aria-expanded", "true");
      document.body.style.overflow = "hidden";
      zablokujTlo(true);
      var first = $(".szuflada__zamknij", drawer);
      if (first) first.focus();
    };
    var closeDrawer = function () {
      drawer.setAttribute("data-open", "false");
      drawer.setAttribute("inert", "");
      navToggle.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
      zablokujTlo(false);
      /* Safari nie daje fokusu klikniętemu przyciskowi - wtedy fokus wraca
         na przycisk "Menu", a nie na <body> */
      var cel = lastFocused && lastFocused !== document.body && document.contains(lastFocused) ? lastFocused : navToggle;
      cel.focus();
    };
    drawer.setAttribute("inert", "");
    navToggle.addEventListener("click", function () {
      drawer.getAttribute("data-open") === "true" ? closeDrawer() : openDrawer();
    });
    $$("[data-drawer-close]", drawer).forEach(function (el) { el.addEventListener("click", closeDrawer); });
    document.addEventListener("keydown", function (e) {
      if (drawer.getAttribute("data-open") !== "true") return;
      if (e.key === "Escape") { closeDrawer(); return; }
      if (e.key === "Tab") {
        /* fokus zostaje w szufladzie */
        var lista = focusable();
        if (!lista.length) return;
        var pierwszy = lista[0], ostatni = lista[lista.length - 1];
        if (e.shiftKey && document.activeElement === pierwszy) { e.preventDefault(); ostatni.focus(); }
        else if (!e.shiftKey && document.activeElement === ostatni) { e.preventDefault(); pierwszy.focus(); }
      }
    });
    /* szuflada zamyka sie po przejsciu do kotwicy na tej samej stronie */
    $$("a[href*='#']", drawer).forEach(function (a) { a.addEventListener("click", closeDrawer); });
  }

  $$("[data-submenu-toggle]").forEach(function (btn) {
    var wDesktopie = !!btn.closest(".menu");
    var wrap = btn.closest(".menu__z-podmenu");
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!open));
    });
    if (!wDesktopie || !wrap) return;
    document.addEventListener("click", function (e) {
      if (!wrap.contains(e.target)) btn.setAttribute("aria-expanded", "false");
    });
    /* Esc zamyka podmenu otwarte przyciskiem albo najechaniem (WCAG 1.4.13);
       klasa schodzi, gdy kursor opusci pozycje */
    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape") return;
      var otwarte = btn.getAttribute("aria-expanded") === "true";
      if (otwarte || wrap.matches(":hover")) {
        btn.setAttribute("aria-expanded", "false");
        wrap.classList.add("esc-zamkniete");
        if (otwarte || wrap.contains(document.activeElement)) btn.focus();
      }
    });
    wrap.addEventListener("mouseleave", function () { wrap.classList.remove("esc-zamkniete"); });
    btn.addEventListener("click", function () { wrap.classList.remove("esc-zamkniete"); });
    /* fokus wychodzi z pozycji - podmenu sie zamyka */
    wrap.addEventListener("focusout", function (e) {
      if (!e.relatedTarget || !wrap.contains(e.relatedTarget)) btn.setAttribute("aria-expanded", "false");
    });
  });

  /* --------------------------------- 3. Czy gabinet teraz przyjmuje */
  /* Czas liczony w strefie Europe/Warsaw (nie wg zegara urzadzenia). Godziny
     w atrybucie data-godziny: "1:9:00-15:00;2:15:00-19:00;..." (1 = poniedzialek)
     - jedno zrodlo z tabela godzin i danymi strukturalnymi. */
  var DNI = { Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6, Sun: 7 };
  var czasWarszawa = function () {
    var dzien = 0, godz = 0, min = 0;
    try {
      new Intl.DateTimeFormat("en-US", { timeZone: "Europe/Warsaw", weekday: "short", hour: "2-digit", minute: "2-digit", hourCycle: "h23" })
        .formatToParts(new Date()).forEach(function (p) {
          if (p.type === "weekday") dzien = DNI[p.value] || 0;
          if (p.type === "hour") godz = Number(p.value) % 24;
          if (p.type === "minute") min = Number(p.value);
        });
    } catch (e) { /* stara przegladarka: zegar urzadzenia */ }
    if (!dzien) { var d = new Date(); dzien = d.getDay() === 0 ? 7 : d.getDay(); godz = d.getHours(); min = d.getMinutes(); }
    return { dzien: dzien, minuty: godz * 60 + min };
  };
  var naMinuty = function (hhmm) {
    var p = String(hhmm).trim().split(":");
    return Number(p[0]) * 60 + Number(p[1] || 0);
  };
  var mapaGodzin = function (raw) {
    var map = {};
    (raw || "").split(";").forEach(function (part) {
      var i = part.indexOf(":");
      if (i < 1) return;
      var zakres = part.slice(i + 1).split("-");
      if (zakres.length === 2) map[Number(part.slice(0, i))] = { od: zakres[0], do: zakres[1] };
    });
    return map;
  };

  var odswiezStan = function () {
    var t = czasWarszawa();
    $$("[data-stan]").forEach(function (el) {
      var map = mapaGodzin(el.getAttribute("data-godziny"));
      if (!Object.keys(map).length) return;
      var dzis = map[t.dzien];
      var tekst = "";
      if (dzis && t.minuty >= naMinuty(dzis.od) && t.minuty < naMinuty(dzis.do)) {
        tekst = napis(el, "otwarte", { godzina: dzis.do });
      } else if (dzis && t.minuty < naMinuty(dzis.od)) {
        tekst = napis(el, "dzis", { godzina: dzis.od });
      } else {
        var nazwy = [""].concat((el.getAttribute("data-napis-dni") || "").split("|"));
        for (var i = 1; i <= 7; i++) {
          var d = ((t.dzien - 1 + i) % 7) + 1;
          if (map[d]) {
            tekst = napis(el, "otwieramy", { dzien: i === 1 ? napis(el, "jutro") : (nazwy[d] || ""), godzina: map[d].od });
            break;
          }
        }
      }
      if (tekst && el.textContent !== tekst) el.textContent = tekst;
      if (tekst) el.hidden = false;
    });
    /* dzisiejszy dzien w paskach tygodnia i tabelach godzin */
    $$("[data-tydzien] [data-dni]").forEach(function (li) {
      var dni = (li.getAttribute("data-dni") || "").split(" ").map(Number);
      li.classList.toggle("jest-dzis", dni.indexOf(t.dzien) > -1);
    });
    $$("table.godziny").forEach(function (tab) {
      $$("tr[data-dzien]", tab).forEach(function (tr) {
        var jest = Number(tr.getAttribute("data-dzien")) === t.dzien;
        tr.classList.toggle("jest-dzis", jest);
        var znak = $(".godziny__dzis", tr);
        if (jest && !znak) {
          znak = document.createElement("span");
          znak.className = "godziny__dzis";
          znak.textContent = napis(tab, "dzis");
          var th = $("th", tr);
          if (th) th.appendChild(znak);
        } else if (!jest && znak) {
          znak.remove();
        }
      });
    });
  };
  odswiezStan();
  var zegar = setInterval(odswiezStan, 60000);
  document.addEventListener("visibilitychange", function () {
    clearInterval(zegar);
    if (!document.hidden) { odswiezStan(); zegar = setInterval(odswiezStan, 60000); }
  });

  /* -------------------------------------------------------- 4. Powiekszanie */
  var lightbox = $("#lightbox");
  if (lightbox) {
    var lbImg = $("[data-lb-img]", lightbox);
    var lbCap = $("[data-lb-cap]", lightbox);
    var lbLicznik = $("[data-lb-licznik]", lightbox);
    var items = $$("[data-lightbox]");
    var index = 0;
    var otwierajacy = null;
    var show = function (i) {
      index = (i + items.length) % items.length;
      var btn = items[index];
      lbImg.src = btn.getAttribute("data-full");
      lbImg.alt = btn.getAttribute("data-alt") || "";
      lbCap.textContent = btn.getAttribute("data-alt") || "";
      if (lbLicznik) lbLicznik.textContent = napis(lightbox, "licznik", { nr: index + 1, razem: items.length });
    };
    items.forEach(function (btn, i) {
      btn.addEventListener("click", function () {
        otwierajacy = btn;
        show(i);
        if (typeof lightbox.showModal === "function") lightbox.showModal();
      });
    });
    $$("[data-lb-prev]", lightbox).forEach(function (b) { b.addEventListener("click", function () { show(index - 1); }); });
    $$("[data-lb-next]", lightbox).forEach(function (b) { b.addEventListener("click", function () { show(index + 1); }); });
    $$("[data-lb-close]", lightbox).forEach(function (b) { b.addEventListener("click", function () { lightbox.close(); }); });
    lightbox.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); show(index + 1); }
      if (e.key === "ArrowLeft") { e.preventDefault(); show(index - 1); }
    });
    lightbox.addEventListener("click", function (e) { if (e.target === lightbox) lightbox.close(); });
    lightbox.addEventListener("close", function () {
      /* fokus wraca na kafel, z ktorego otwarto zdjecie */
      var cel = items[index] || otwierajacy;
      if (cel) cel.focus();
    });
  }

  /* ------------------------------------------------------------- 5. Mapa */
  /* Ramka Google powstaje dopiero po swiadomym kliknieciu (adres IP pacjenta
     nie trafia do Google wczesniej). Tytul ramki z parametru q adresu mapy. */
  var tytulMapy = function (box, src) {
    var adres = "";
    try { adres = new URL(src, location.href).searchParams.get("q") || ""; } catch (e) { /* stara przegladarka */ }
    return napis(box, "tytul") + (adres ? ": " + adres : "");
  };
  $$("[data-map]").forEach(function (box) {
    var btn = $("[data-map-load]", box);
    if (!btn) return;
    var zapamietana = false;
    btn.addEventListener("click", function () {
      /* przycisk znika z DOM - fokus przechodzi na ramke mapy (tylko po
         kliknieciu, nie przy wczytaniu z zapamietanej zgody) */
      var przeniesFokus = !zapamietana;
      var frame = document.createElement("iframe");
      frame.src = box.getAttribute("data-map-src");
      frame.title = tytulMapy(box, frame.src);
      frame.loading = "lazy";
      frame.referrerPolicy = "no-referrer-when-downgrade";
      frame.setAttribute("allowfullscreen", "");
      box.innerHTML = "";
      box.appendChild(frame);
      if (przeniesFokus) { box.setAttribute("tabindex", "-1"); box.focus({ preventScroll: true }); }
      try { sessionStorage.setItem("mapa-zgoda", "1"); } catch (e) { /* tryb prywatny */ }
    });
    try { if (sessionStorage.getItem("mapa-zgoda") === "1") { zapamietana = true; btn.click(); } } catch (e) { /* tryb prywatny */ }
  });

  /* ------------------------------------------------------ 6. Filtr cennika */
  var priceSearch = $("[data-price-search]");
  var table = $("#cennik-tabela");
  if (priceSearch && table) {
    var tools = $("[data-price-tools]");
    if (tools) tools.hidden = false;
    var counter = $("[data-price-count]");
    var pusto = $("[data-price-empty]");
    var rows = $$("tr.cennik__pozycja", table);
    var groups = $$("tbody[data-grupa]", table);
    /* "zab" znajduje "ząb", "lacz" - "łącz"; twarde spacje (sklad.html)
       licza sie jak zwykle */
    var bezOgonkow = function (s) {
      return s.toLowerCase().replace(/ł/g, "l").normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/\s+/g, " ");
    };
    rows.forEach(function (tr) { tr.setAttribute("data-szukaj", bezOgonkow(tr.textContent)); });
    var filter = function () {
      var q = bezOgonkow(priceSearch.value.trim());
      var shown = 0;
      rows.forEach(function (tr) {
        var hit = !q || tr.getAttribute("data-szukaj").indexOf(q) > -1;
        tr.hidden = !hit;
        if (hit) shown++;
      });
      groups.forEach(function (g) {
        g.hidden = !$$("tr.cennik__pozycja", g).some(function (tr) { return !tr.hidden; });
      });
      if (counter) {
        counter.textContent = q
          ? napis(counter, "pasujace", { liczba: shown, razem: rows.length })
          : napis(counter, "wszystkie", { liczba: rows.length });
      }
      if (pusto) pusto.hidden = !(q && shown === 0);
    };
    priceSearch.addEventListener("input", filter);
    $$("[data-price-clear]").forEach(function (b) {
      b.addEventListener("click", function () { priceSearch.value = ""; filter(); priceSearch.focus(); });
    });
    filter();
  }

  /* ---------------------------------------------- 7. Formularz kontaktowy */
  /* Formularz niczego nie wysyla (brak obslugi na serwerze) - jak v1. */
  $$("[data-demo-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var box = form.nextElementSibling;
      if (box && box.hasAttribute("data-form-result")) {
        box.hidden = false;
        box.focus();
        box.scrollIntoView({ block: "center", behavior: ruch ? "smooth" : "auto" });
      }
      form.hidden = true;
    });
  });

  /* -------------------------------------------------- 8. Rok w stopce */
  $$("[data-rok]").forEach(function (el) { el.textContent = String(new Date().getFullYear()); });

  /* --------------------------- 9. Pasek glowny po przewinieciu (ton tla) */
  var naglowek = $("[data-naglowek]");
  if (naglowek) {
    var ton = function () { naglowek.classList.toggle("przewiniety", window.scrollY > 8); };
    window.addEventListener("scroll", ton, { passive: true });
    ton();
  }

  /* -------------- 10. Dolny pasek: chowany, gdy karta albo cta sa widoczne */
  var pasek = $("[data-pasek-dolny]");
  var cele = $$("[data-karta-hero], .s--cta");
  if (pasek && cele.length && "IntersectionObserver" in window) {
    var naEkranie = [];
    var obsPaska = new IntersectionObserver(function (wpisy) {
      wpisy.forEach(function (w) {
        var i = naEkranie.indexOf(w.target);
        if (w.isIntersecting && i < 0) naEkranie.push(w.target);
        if (!w.isIntersecting && i > -1) naEkranie.splice(i, 1);
      });
      ustawPasek();
    }, { threshold: 0 });
    cele.forEach(function (el) { obsPaska.observe(el); });
  }
  /* przy przewijaniu w dol pasek ustepuje tresci, przy przewijaniu w gore wraca */
  var wDol = false, ostatnieY = window.scrollY;
  function ustawPasek() {
    if (!pasek) return;
    var ukryty = wDol || (typeof naEkranie !== "undefined" && naEkranie.length > 0);
    pasek.classList.toggle("pasek-dolny--ukryty", ukryty);
    /* schowany pasek nie przyjmuje fokusu (odnosniki poza ekranem) */
    if (ukryty) pasek.setAttribute("inert", ""); else pasek.removeAttribute("inert");
  }
  if (pasek) {
    wDol = window.scrollY < (window.innerHeight || 800) * 0.8;
    ustawPasek();
    window.addEventListener("scroll", function () {
      var y = window.scrollY;
      if (Math.abs(y - ostatnieY) < 6) return;
      /* pasek pojawia sie dopiero za pierwszym ekranem (na nim telefon jest
         w naglowku) i chowa sie przy przewijaniu w dol */
      wDol = (y > ostatnieY) || y < (window.innerHeight || 800) * 0.8;
      ostatnieY = y;
      ustawPasek();
    }, { passive: true });
  }

  /* rzeczywista wysokosc paska (rosnie przy wiekszym tekscie) - rezerwa
     w stopce i scroll-padding-bottom w CSS; naglowek wyzszy niz 1/5 okna
     przestaje sie przyklejac */
  var mierz = function () {
    if (pasek && pasek.offsetHeight) root.style.setProperty("--wys-paska-dolnego", pasek.offsetHeight + "px");
    if (naglowek) naglowek.classList.toggle("naglowek--luzny", naglowek.offsetHeight > (window.innerHeight || 800) * 0.2);
  };
  mierz();
  if ("ResizeObserver" in window) {
    var obsWys = new ResizeObserver(mierz);
    if (pasek) obsWys.observe(pasek);
    if (naglowek) obsWys.observe(naglowek);
  }
  window.addEventListener("resize", mierz, { passive: true });
  /* fokus pod widocznym paskiem: strona przewija sie o brakujacy kawalek */
  if (pasek) {
    document.addEventListener("focusin", function (e) {
      var el = e.target;
      if (!el || !el.getBoundingClientRect || pasek.contains(el) || pasek.classList.contains("pasek-dolny--ukryty")) return;
      if (getComputedStyle(pasek).position !== "fixed") return;
      var roznica = el.getBoundingClientRect().bottom - pasek.getBoundingClientRect().top;
      if (roznica > 0) window.scrollBy(0, roznica + 16);
    });
  }

  /* ------------------------------------------- 11. Spis tresci: aktywna */
  $$("[data-spis]").forEach(function (spis) {
    if (!("IntersectionObserver" in window)) return;
    var linki = $$("a[href^='#']", spis);
    var cele = linki.map(function (a) { return document.getElementById(decodeURIComponent(a.getAttribute("href").slice(1))); });
    var aktywne = function (id) {
      linki.forEach(function (a) { a.classList.toggle("aktywny", a.getAttribute("href") === "#" + id); });
    };
    var obs = new IntersectionObserver(function (wpisy) {
      var wejscie = wpisy.filter(function (w) { return w.isIntersecting; })
        .sort(function (a, b) { return a.boundingClientRect.top - b.boundingClientRect.top; })[0];
      if (wejscie) aktywne(wejscie.target.id);
    }, { rootMargin: "-20% 0px -60% 0px" });
    cele.forEach(function (c) { if (c) obs.observe(c); });
  });

  /* ---------------------------- 12. Listy rozwijane (spis, kategorie) */
  /* Bez skryptu lista jest widoczna, a przycisk ukryty. */
  $$("[data-rozwin]").forEach(function (btn) {
    var lista = document.getElementById(btn.getAttribute("aria-controls"));
    if (!lista) return;
    var ustaw = function (otwarta) {
      btn.setAttribute("aria-expanded", String(otwarta));
      lista.hidden = !otwarta;
    };
    btn.hidden = false;
    ustaw(false);
    btn.addEventListener("click", function () { ustaw(btn.getAttribute("aria-expanded") !== "true"); });
    /* po wyborze pozycji lista sie zwija */
    $$("a", lista).forEach(function (a) { a.addEventListener("click", function () { ustaw(false); }); });
  });

  /* ------------------------------------------------------- 13. Ruch */
  /* Stan ukryty jest w CSS tylko pod .js i "prefers-reduced-motion:
     no-preference"; bez skryptu i przy ograniczonym ruchu nic nie czeka. */
  var mozaika = $("[data-mozaika]");
  var odslon = function (el) { el.classList.add("widoczne"); };
  /* zdjecia galerii (data-wejscie-kafle) odslaniaja sie kafel po kaflu */
  var wszystkie = $$("[data-wejscie-krok], [data-wejscie-lista], [data-wejscie-kafle] > *");
  var toKafel = function (el) { return el.parentNode && el.parentNode.hasAttribute && el.parentNode.hasAttribute("data-wejscie-kafle"); };

  if (!ruch || !("IntersectionObserver" in window)) {
    wszystkie.forEach(odslon);
    if (mozaika) mozaika.classList.add("ulozona");
  } else {
    /* druk sie uklada: kafle mozaiki kolejno (tuz po pierwszym malowaniu) */
    if (mozaika) requestAnimationFrame(function () { requestAnimationFrame(function () { mozaika.classList.add("ulozona"); }); });

    /* kroki i pozycje list */
    var wysokosc = window.innerHeight || root.clientHeight;
    var obserwator = new IntersectionObserver(function (wpisy) {
      wpisy.filter(function (w) { return w.isIntersecting; })
        .map(function (w) { return w.target; })
        .sort(function (a, b) { return a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1; })
        .forEach(function (el, i) {
          if (!el.hasAttribute("data-wejscie-lista")) el.style.setProperty("--opoznienie", Math.min(i, 5) * 70 + "ms");
          odslon(el);
          obserwator.unobserve(el);
        });
    }, { rootMargin: "0px 0px -10% 0px" });
    var kafleNaEkranie = 0;
    wszystkie.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < wysokosc && r.bottom > 0 && toKafel(el)) {
        /* kafle nad zgieciem: od razu, kolejno (animacja CSS) */
        el.style.setProperty("--opoznienie", Math.min(kafleNaEkranie++, 6) * 70 + "ms");
        odslon(el);
      } else if (r.top < wysokosc && r.bottom > 0) {
        /* tresc nad zgieciem nie czeka */
        el.classList.add("bez-przejscia");
        odslon(el);
        requestAnimationFrame(function () { requestAnimationFrame(function () { el.classList.remove("bez-przejscia"); }); });
      } else {
        obserwator.observe(el);
      }
    });
    var odslonDo = function (cel) {
      if (!cel) return;
      wszystkie.forEach(function (el) {
        if (el === cel || el.contains(cel) || cel.contains(el) || (el.compareDocumentPosition(cel) & Node.DOCUMENT_POSITION_FOLLOWING)) {
          odslon(el); obserwator.unobserve(el);
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
      var el = e.target.closest && e.target.closest("[data-wejscie-krok]:not(.widoczne), [data-wejscie-lista]:not(.widoczne), [data-wejscie-kafle] > :not(.widoczne)");
      if (el) odslonDo(el);
    });
    window.addEventListener("beforeprint", function () { wszystkie.forEach(odslon); });
  }

  root.classList.add("js-gotowy");
})();
