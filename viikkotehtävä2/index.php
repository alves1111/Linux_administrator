<?php
// Yhdistetään MariaDB-tietokantaan
$db = new mysqli("localhost", "lempuser", "******", "lempdb");

if ($db->connect_error) {
    $kellonaika = "Tietokantavirhe: " . htmlspecialchars($db->connect_error);
} else {
    $result = $db->query("SELECT NOW() AS aika");
    if ($result) {
        $row = $result->fetch_assoc();
        $kellonaika = $row['aika'];
    } else {
        $kellonaika = "Virhe SQL-kyselyssä.";
    }
    $db->close();
}
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Viikkotehtävä 2</title>
    <style>
        body {
            background: linear-gradient(to bottom right, #7dd3fc, #38bdf8);
            font-family: Arial, sans-serif;
            text-align: center;
            padding-top: 60px;
        }
        h1 { color: #0c4a6e; }
        .card {
            background: white;
            padding: 30px;
            margin: 40px auto;
            border-radius: 20px;
            width: 60%;
            max-width: 700px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        }
        img {
            width: 400px;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            margin-top: 20px;
        }
        .joke {
            font-style: italic;
            color: #0c4a6e;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <h1>Viikkotehtävä 2</h1>

    <img src="https://images.sanoma-sndp.fi/2d9ea41bfd904f11a32b7809a1c1fa75.jpg/normal/978.avif"
    </p>

    <div class="card">
        <h2>Anna vitonen</h2>
        <p>Kello on jossain päin maailmaa tämän verran: <b><?php echo htmlspecialchars($kellonaika); ?></b></p>
    </div>
</body>
</html>
