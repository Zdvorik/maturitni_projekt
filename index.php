<?php
// Implementování logiky
require_once('core.php');
?>

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>The Snake</title>

  <!-- Bootstrap 5.3.3 -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.min.js" integrity="sha384-0pUGZvbkm6XF6gxjEnlmuGrJXVbNuzT9qBBavbLwCsOGabYfZo0T0to5eqruptLy" crossorigin="anonymous"></script>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous" />

  <!-- Vlastní styl -->
  <link rel="stylesheet" href="style.css" />
</head>

<body>

  <!-- Modal pro přihlášení -->
  <div class="modal fade" id="loginModal" tabindex="-1" role="dialog" aria-labelledby="loginModalLabel" aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header bg-dark">
          <h5 class="modal-title" id="loginModalLabel">Přihlásit se</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body bg-dark text-center">
          <form action="index.php" method="post">
            <div class="form-group">
            <label for="user">Uživatelské jméno</label>
              <input type="text" name="user" placeholder="Uživatelské jméno" class="form-control">
              </div>
              <div class="form-group">
              <label for="password">Heslo</label>
              <input type="password" name="password" placeholder="Heslo" class="form-control">
            </div>
            <button type="submit" class="btn btn-primary">Přihlásit se</button>
          </form>
        </div>
      </div>
    </div>
  </div>

  <!-- Lišta na horní části stránky -->
  <nav class="navbar navbar-expand-sm">
    <div class="container">
      <a href="https://new.spskladno.cz"><img src="https://new.spskladno.cz/wp-content/uploads/2020/08/vos-sps-kladno-logo-5.png" alt="Logo" height="50" /></a>
      <h1 class="title">The Snake</h1>

      <?php if (!isset($_SESSION['user'])): ?>
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#loginModal">Přihlásit</button>
      <?php else: ?>
        <a class="btn btn-primary" href="index.php?logout=true">Odhlásit se!</a>
      <?php endif; ?>
    </div>
  </nav>


  <!-- Hlavní obsah stránky -->
  <main>
    <div class="container">
      <h2>O hře</h2>
      <p>
        Snake je klasická arkádová hra, ve které ovládáte hada pohybujícího se po hrací ploše. Cílem je sbírat potravu (body) a tím prodlužovat jeho délku, přičemž se musíte vyhýbat nárazu do stěn a vlastního těla. Hra se postupně stává obtížnější, protože s rostoucí délkou hada máte méně prostoru
        k pohybu. Ovládání je jednoduché – obvykle se používají šipky na klávesnici nebo dotykové ovládání.
      </p>
      <div class="separator"></div>
      <h3>Nejlepší hráči</h3>

      <!-- Tabulka se skórem -->
      <?php print_table(); ?>
      <div class="separator"></div>

      <h2>Informace o projektu + použité knihovny</h2>
      <p>
        Tento projekt představuje komplexní aplikaci v jazyce Python s webovým rozhraním a databázovou správou, která umožňuje uživatelům interaktivní práci s daty. Projekt je navržen jako skupinová nebo samostatná práce, splňující požadavky na moderní softwarový vývoj.

        Hlavní funkce projektu:
      <ul>
        <li>Webová prezentace projektu s popisem, ukázkami a dokumentací.</li>
        <li>Uživatelská autentizace s rozdílnými úrovněmi přístupu (běžný uživatel, administrátor).</li>
        <li>Databázová správa s podporou CRUD operací (vkládání, čtení, úprava, mazání dat).</li>
        <li>Grafické rozhraní vytvořené pomocí PyQt nebo jiného frameworku.</li>
        <li>Zpracování a vizualizace dat pomocí Pygame nebo knihoven pro generování grafů.</li>
        <li>Práce s GITem, dokumentace kódu a uložení projektu na repozitář.</li>
        <li>Projekt je postaven na technologiích Python, HTML/CSS/JavaScript/Bootstrap, PHP a MariaDB, s důrazem na modularitu, bezpečnost a efektivní práci s databázemi.</li>
        <li>Celý projekt je dokumentován na <a href="https://github.com/Zdvorik/maturitni_projekt">TOMTO</a> gitu.</li>
      </ul>
      </p>
      <img src="assets/diagram.png" alt="Diagram" class="mx-auto d-block img-responsive diagram" />
      <br>
      <img src="assets/erMOdel.png" alt="e-r model" class="mx-auto d-block img-responsive diagram" />
    </div>
  </main>

  <!-- Footer Copyright + vytvořil -->
  <footer>
    &copy; <?php echo date("Y"); ?> The Snake, Vytvořil Matěj Zdvoráček
  </footer>

  <!-- Vlastní skript -->
  <script src="script.js"></script>
</body>

</html>
