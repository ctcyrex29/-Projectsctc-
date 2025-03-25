<?php
// PHP script to call the Flask API
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Get symptoms from the POST request
    $symptoms = $_POST['symptoms']; // Assuming symptoms are sent as a POST parameter

    // Prepare the data to send in JSON format
    $data = json_encode(['symptoms' => $symptoms]);

    // Initialize cURL session
    $ch = curl_init();

    // Correct the URL to the Flask API endpoint
    $url = 'http://127.0.0.1:5000/diagnose';  // Correct URL for Flask API (assuming Flask runs locally)

    // Set the cURL options
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'Content-Length: ' . strlen($data)
    ]);

    // Execute the request and get the response
    $response = curl_exec($ch);

    // Error handling: Check if cURL request was successful
    if ($response === false) {
        echo "cURL Error: " . curl_error($ch);
    } else {
        // Decode the response (which is JSON) into a PHP array
        $result = json_decode($response, true);

        // Check if the result is valid and not empty
        if (isset($result['message'])) {
            // Display error message from Flask API (e.g., "No matching diseases found")
            $diagnosis_message = htmlspecialchars($result['message']);
        } else {
            // Store the diagnosis result
            $diagnosis_message = null;
            $diagnosis_result = $result;
        }
    }

    // Close cURL session
    curl_close($ch);
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health Diagnosis</title>
</head>
<body>
    <h1>Health Diagnosis Form</h1>

    <!-- Form to collect symptoms -->
    <form action="diagnose.php" method="POST">
        <h3>Enter Symptoms:</h3>
        <div id="symptoms-container">
            <input type="text" name="symptoms[]" placeholder="Enter symptom" required>
        </div>
        <button type="button" onclick="addTextbox()">Add Another Symptom</button>

        <br><br>
        <input type="submit" value="Submit">
    </form>

    <script>
        // Function to add more symptom input boxes
        function addTextbox() {
            var container = document.getElementById('symptoms-container');
            var input = document.createElement('input');
            input.type = 'text';
            input.name = 'symptoms[]';
            input.placeholder = 'Enter symptom';
            container.appendChild(input);
        }
    </script>

    <!-- Display Results Below Form -->
    <div id="diagnosis-result">
        <?php if (isset($diagnosis_message)): ?>
            <!-- If there is a message (like no matching diseases) -->
            <h3>Diagnosis Result:</h3>
            <p><?php echo $diagnosis_message; ?></p>
        <?php elseif (isset($diagnosis_result) && !empty($diagnosis_result)): ?>
            <!-- If there are matching diseases -->
            <h3>Diagnosis Results:</h3>
            <pre>
            <?php
            foreach ($diagnosis_result as $disease) {
                echo "<strong>Disease:</strong> " . htmlspecialchars($disease['name']) . "<br>";
                echo "<strong>Matched Symptoms:</strong> " . $disease['matched_symptoms'] . "<br>";

                // Check if causes exist and display them
                if (isset($disease['causes']) && !empty($disease['causes'])) {
                    echo "<strong>Causes:</strong> <ul>";
                    foreach ($disease['causes'] as $cause) {
                        echo "<li>" . htmlspecialchars($cause) . "</li>";
                    }
                    echo "</ul>";
                } else {
                    echo "<strong>Causes:</strong> Not available<br>";
                }

                // Check if medications exist and display them
                if (isset($disease['medications']) && !empty($disease['medications'])) {
                    echo "<strong>Medications:</strong> <ul>";
                    foreach ($disease['medications'] as $medication) {
                        echo "<li>" . htmlspecialchars($medication) . "</li>";
                    }
                    echo "</ul>";
                } else {
                    echo "<strong>Medications:</strong> Not available<br>";
                }
                echo "<hr>";
            }
            ?>
            </pre>
        <?php endif; ?>
    </div>
</body>
</html>
