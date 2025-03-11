<?php
$login_username = "admin";
$login_password = "admin";

session_start();

// Proměné pro připojení k databázi
$database_hostname = "dbs.spskladno.cz";
$database_port = 3306;
$database_username = "student16";
$database_password = "spsnet";
$database_name = "vyuka16";
$database_table_users = "snk_users";
$database_table_scores = "snk_scores";
$database_connection = database_connect();

handle_actions();

// Připojí se k databázi
function database_connect()
{
    global $database_hostname, $database_port, $database_username, $database_password, $database_name;
    $conn = new mysqli($database_hostname, $database_username, $database_password, $database_name, $database_port);
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    return $conn;
}

// Zpracuje akce z formuláře
function handle_actions()
{
    if ($_SERVER["REQUEST_METHOD"] === "POST") {
        if (isset($_POST['user']) && isset($_POST['password'])) {
            login();
        }
    } else if ($_SERVER["REQUEST_METHOD"] === "GET") {
        if (isset($_GET['logout'])) {
            logout();
        } else if (isset($_GET['delete'])) {
            remove_score($_GET['delete']);
        } else if (isset($_GET['alert'])) {
            show_alert($_GET['alert']);
        }
    }
}

// Přihlásí uživatele
function login()
{
    global $login_username, $login_password;
    $user_name = trim($_POST['user']);
    $user_password = trim($_POST['password']);
    if (empty($user_name) || empty($user_password)) {
        header("Location: index.php?alert=empty_credentials");
        exit();
    }

    if ($user_name !== $login_username || $user_password !== $login_password) {
        header("Location: index.php?alert=invalid_credentials");
        exit();
    }

    $_SESSION['user'] = $user_name;
    header("Location: index.php?alert=login");
    exit();
}

// Odhlasí uživatele
function logout()
{
    if (isset($_SESSION['user'])) {
        unset($_SESSION['user']);
        header("Location: index.php?alert=logout");
        exit();
    }
}

// Vytiskne tabulku s nejlepšími skóre
function print_table()
{
    global $database_table_users, $database_table_scores;
    $sql = "SELECT s.user_id, s.score, s.time, u.username 
            FROM `" . $database_table_scores . "` AS s 
            INNER JOIN `" . $database_table_users . "` AS u ON s.user_id = u.user_id 
            ORDER BY s.score DESC, s.time ASC LIMIT 10;";
    
    global $database_connection;
    $result = $database_connection->query($sql);

    echo "<table class='table table-bordered table-dark table-hover'>";
    echo "<thead><tr><th scope='col'>Hráč</th><th scope='col'>Skóre</th><th scope='col'>Čas</th>";
    
    if (isset($_SESSION['user'])) {
        echo "<th scope='col'>Smazat</th>";
    }
    echo "</tr></thead><tbody>";
    
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $time = $row['time'];
            $minutes = floor($time / 60);
            $seconds = $time % 60;
            
            echo get_table_row($row['username'], $row['user_id'], $row['score'], $minutes . "m " . $seconds . "s");
        }
    }
    
    echo "</tbody></table>";
}

// Vytvoří řádek tabulky s informacemi o skóre
function get_table_row($name, $user_id, $score, $time)
{
    $row = "<tr>";
    $row .= "<th>$name</th>";
    $row .= "<td>$score</td>";
    $row .= "<td>$time</td>";
    if (isset($_SESSION['user'])) {
        $row .= '<td><a href="index.php?delete=' . $user_id . '" class="btn-delete">❌</a></td>';
    }
    $row .= "</tr>";
    return $row;
}

// Odstraní skóre z databáze
function remove_score($user_id)
{
    global $database_table_users;
    $sql = "DELETE FROM `" . $database_table_users . "` WHERE user_id = " . $user_id;
    global $database_connection;
    $database_connection->query($sql);
    header("Location: index.php?alert=delete");
    exit();
}

// Zobrazí alert box na horní části stránky
function show_alert($type)
{
    if ($type === "login") {
        send_alert("success", "Úspěšné přihlášení. Vítej " . $_SESSION['user']);
    } else if ($type === "logout") {
        send_alert("success", "Odhlášení proběhlo úspěšně");
    } else if ($type === "delete") {
        send_alert("success", "Skóre bylo smazáno");
    } else if ($type === "empty_credentials") {
        send_alert("danger", "Vyplňte prosím všechna pole");
    } else if ($type === "invalid_credentials") {
        send_alert("danger", "Neplatné přihlašovací údaje");
    }

    // Přesmerování na index.php za 5 sekund
    header("refresh:5;url=index.php");
}

// Vloží alert box na stránku
function send_alert($type, $message)
{
    echo '<div class="alert alert-' . $type . ' text-center" role="alert">' . $message . '</div>';
}
