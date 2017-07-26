<!-- http://www.w3schools.com/w3css/default.asp -->

<!DOCTYPE html>
<html>
<title>Mood tracker</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="static/css/W3.css">
<body class="w3-light-grey">

<div class="w3-content" style="max-width:1400px">

  <!-- Header -->
  <div class="w3-container w3-center w3-padding-2">
    <h2>Here are all results so far:</h2>
  </div>

  <!-- Symptoms table -->
  <div class="w3-container w3-padding-16">
    <div class="w3-card-2 w3-white w3-responsive w3-tiny">
      <table class="w3-table-all">

        <!-- Put generated header data here -->
        <tr class="w3-orange">
          {{!column_data}}
        </tr>

        <!-- Put generated table data here -->
        {{!table_data}}
      </table>
    </div>
  </div>
</div>
</body>
</html>
