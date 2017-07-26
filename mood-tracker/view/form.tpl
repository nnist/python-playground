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
    <h2>How are you feeling?</h2>
  </div>

  <form class="" action="/submit" method="post">

  <!-- Symptoms table -->
  <div class="w3-container w3-padding-16">
    <div class="w3-card-2 w3-white">

      <div class="w3-container w3-orange">
        <h4>Symptoms</h4>
      </div>

      <div class="w3-panel w3-blue">
        <p>Severities:</p>
        <ol>
          <li>Symptom not present</li>
          <li>Present, but very manageable</li>
          <li>Quite severe, but still able to cope</li>
          <li>Severe, unable to cope</li>
        </ol>
      </div>

      <table class="w3-table w3-bordered w3-centered">

        <tr>
          <th></th>
          <th>0</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
        </tr>

        <!-- Depression -->
        <tr>
          <td class="w3-padding-large w3-left-align">Depression</td>
          <td><label class="w3-white w3-padding-small"><input class="w3-radio" type="radio" name="depression" value="0" required></label></td>
          <td><label class="w3-white w3-padding-small"><input class="w3-radio" type="radio" name="depression" value="1"></label></td>
          <td><label class="w3-white w3-padding-small"><input class="w3-radio" type="radio" name="depression" value="2"></label></td>
          <td><label class="w3-white w3-padding-small"><input class="w3-radio" type="radio" name="depression" value="3"></label></td>
        </tr>

        <!-- Mania -->
        <tr>
          <td class="w3-padding-large w3-left-align">Mania</td>
          <td><label class="w3-white w3-padding-small"><input class="w3-radio" type="radio" name="mania" value="0" required></label></td>
          <td><label class="w3-white w3-padding-small"><input class="w3-radio" type="radio" name="mania" value="1"></label></td>
          <td><label class="w3-white w3-padding-small"><input class="w3-radio" type="radio" name="mania" value="2"></label></td>
          <td><label class="w3-white w3-padding-small"><input class="w3-radio" type="radio" name="mania" value="3"></label></td>
        </tr>

        <!-- Irritability -->
        <tr>
          <td class="w3-padding-large w3-left-align">Irritability</td>
          <td><label class="w3-white w3-padding-small"><input class="w3-radio" type="radio" name="irritability" value="0" required></label></td>
          <td><label class="w3-white w3-padding-small"><input class="w3-radio" type="radio" name="irritability" value="1"></label></td>
          <td><label class="w3-white w3-padding-small"><input class="w3-radio" type="radio" name="irritability" value="2"></label></td>
          <td><label class="w3-white w3-padding-small"><input class="w3-radio" type="radio" name="irritability" value="3"></label></td>
        </tr>

        <!-- Anxiety -->
        <tr>
          <td class="w3-padding-large w3-left-align">Anxiety</td>
          <td><label class="w3-white w3-padding-small"><input class="w3-radio" type="radio" name="anxiety" value="0" required></label></td>
          <td><label class="w3-white w3-padding-small"><input class="w3-radio" type="radio" name="anxiety" value="1"></label></td>
          <td><label class="w3-white w3-padding-small"><input class="w3-radio" type="radio" name="anxiety" value="2"></label></td>
          <td><label class="w3-white w3-padding-small"><input class="w3-radio" type="radio" name="anxiety" value="3"></label></td>
        </tr>

      </table>
    </div>
  </div>

  <!-- Social meter -->
  <div class="w3-container w3-half w3-padding-16">
    <div class="w3-card-2 w3-white">

      <div class="w3-container w3-orange">
        <h4>Social</h4>
      </div>

      <div class="w3-panel w3-blue">
        <p>P is used to note if anyone else was involved with the activity.</p>
        <ol start="0">
          <li>Alone</li>
          <li>Someone else was present, without interaction</li>
          <li>Someone else was present, with interaction</li>
          <li>Someone else stimulated you</li>
        </ol>
      </div>

      <div class="w3-container">
        <table class="w3-table w3-bordered">
            <tr>
              <th>Activity</th>
              <th>Time</th>
              <th>P</th>
            </tr>
            <tr>
              <td>Waking up</td>
              <td><input class="w3-input w3-border w3-round-medium" type="time" name="waking_up_time"></td>
              <td><input class="w3-input w3-border w3-round-medium" type="number" name="waking_up_p" min="0" max="3"></td>
            </tr>
            <tr>
              <td>First contact</td>
              <td><input class="w3-input w3-border w3-round-medium" type="time" name="first_contact_time"></td>
              <td><input class="w3-input w3-border w3-round-medium" type="number" name="first_contact_p" min="0" max="3"></td>
            </tr>
            <tr>
              <td>Start work</td>
              <td><input class="w3-input w3-border w3-round-medium" type="time" name="start_work_time"></td>
              <td><input class="w3-input w3-border w3-round-medium" type="number" name="start_work_p" min="0" max="3"></td>
            </tr>
            <tr>
              <td>Dinner</td>
              <td><input class="w3-input w3-border w3-round-medium" type="time" name="dinner_time"></td>
              <td><input class="w3-input w3-border w3-round-medium" type="number" name="dinner_p" min="0" max="3"></td>
            </tr>
            <tr>
              <td>Bedtime</td>
              <td><input class="w3-input w3-border w3-round-medium" type="time" name="bedtime_time"></td>
              <td><input class="w3-input w3-border w3-round-medium" type="number" name="bedtime_p" min="0" max="3"></td>
            </tr>
        </table>
      </div>
    </div>
  </div>

  <!-- Optional fields -->
  <div class="w3-container w3-half w3-padding-16">
    <div class="w3-card-2 w3-white">

      <!-- Header -->
      <div class="w3-container w3-orange">
        <h4>Optional</h4>
      </div>

      <div class="w3-row">

        <!-- Weight -->
        <div class="w3-container w3-half">
          <p><input class="w3-input w3-border w3-round-medium" type="number" name="weight" placeholder="Weight" min="0"></p>
        </div>

        <!-- Checkboxes -->
        <div class="w3-container w3-half">
          <p>
            <input class="w3-check" type="checkbox" id="drugs_checkbox" name="drugs">
            <label for="drugs_checkbox" class="w3-validate">Drugs</label>
          </p><p>
            <input class="w3-check" type="checkbox" id="alcohol_checkbox" name="alcohol">
            <label for="alcohol_checkbox" class="w3-validate">Alcohol</label>
          </p><p>
            <input class="w3-check" type="checkbox" id="psychotic_checkbox" name="psychotic">
            <label for="psychotic_checkbox" class="w3-validate">Psychotic symptoms</label>
          </p>
        </div>
      </div>
    </div>
  </div>

  <!-- Notes -->
  <div class="w3-container w3-half w3-padding-16">
    <div class="w3-card-2 w3-white">
      <div class="w3-container w3-orange">
        <h4>Notes</h4>
      </div>
      <div class="w3-container w3-padding-8">
        <textarea class="w3-input w3-border w3-round-medium" name="notes" type="text" rows="3" placeholder="Got any notes?"></textarea>
      </div>
    </div>
  </div>

  <!-- Submit button -->
  <div class="w3-container w3-center w3-padding-16">
    <input class="w3-btn w3-round-large w3-blue w3-xxlarge" value="Save" type="submit">
  </div>

  </form>
</div>
</body>
</html>
