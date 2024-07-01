html = """


Copy code
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Travel Certificate for Non-Citizens</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
        }
        .container {
            width: 100%;
            border: 1px solid #000;
            padding: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .header img {
            max-width: 100px;
        }
        .header h1 {
            font-size: 24px;
            margin: 0;
        }
        .header h2 {
            font-size: 18px;
            margin: 0;
        }
        .notes {
            font-size: 12px;
            margin-bottom: 20px;
        }
        .form-section {
            margin-bottom: 10px;
        }
        .form-section label {
            display: block;
            font-weight: bold;
        }
        .form-section input {
            width: 100%;
            padding: 5px;
            margin-top: 5px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="{{ image_url }}" alt="Republic of Botswana Logo">
            <h1>IMMIGRATION AND PASSPORT CONTROL DIVISION</h1>
            <h2>TRAVEL CERTIFICATE FOR NON-CITIZENS</h2>
        </div>
        <div class="notes">
            <p>(1) A Travel Certificate for Repatriation or Deportation of Aliens and foreign nationals without Travel Documents of their Home Countries shall be issued by Immigration Officers.</p>
            <p>(2) The purpose of the Travel Certificate is to enable holder to travel to his/her Home Country for purpose of permanent residence as a returning national of that country.</p>
            <p>(3) This Travel Certificate is an administrative document issued to non-citizens in the absence of a valid Passport of his/her Home Country.</p>
            <p>(4) In the event of doubt as regards a personal nationality, the Botswana Immigration Authorities will gladly accept the return of the person on production of satisfactory explanation clearly indicating reasons for refusal to accept him/her as a national of that country.</p>
            <p>(5) Non-Citizen's Travel Certificate shall embody his/her antecedents and a full-face photograph of holder.</p>
        </div>
        <div class="form-section">
            <label for="surname">1. SURNAME:</label>
            <input type="text" id="surname" name="surname">
        </div>
        <div class="form-section">
            <label for="other-names">2. OTHER NAMES:</label>
            <input type="text" id="other-names" name="other-names">
        </div>
        <div class="form-section">
            <label for="dob">3. DATE OF BIRTH:</label>
            <input type="text" id="dob" name="dob">
        </div>
        <div class="form-section">
            <label for="pob">4. PLACE OF BIRTH:</label>
            <input type="text" id="pob" name="pob">
        </div>
        <div class="form-section">
            <label for="origin">5. COUNTRY OF ORIGIN:</label>
            <input type="text" id="origin" name="origin">
        </div>
        <div class="form-section">
            <label for="nationality">6. PRESENT NATIONALITY:</label>
            <input type="text" id="nationality" name="nationality">
        </div>
        <div class="form-section">
            <label for="home-address">7. ORIGINAL HOME ADDRESS:</label>
            <input type="text" id="home-address" name="home-address">
        </div>
        <div class="form-section">
            <label for="father-names">8. FATHER'S FULL NAMES:</label>
            <input type="text" id="father-names" name="father-names">
        </div>
        <div class="form-section">
            <label for="father-address">9. FATHER'S FULL ADDRESS:</label>
            <input type="text" id="father-address" name="father-address">
        </div>
        <div class="form-section">
            <label for="mother-names">10. MOTHER'S FULL NAMES:</label>
            <input type="text" id="mother-names" name="mother-names">
        </div>
        <div class="form-section">
            <label for="mother-address">11. MOTHER'S FULL ADDRESS:</label>
            <input type="text" id="mother-address" name="mother-address">
        </div>
        <div class="form-section">
            <label for="relatives">12. NAMES OF OTHER LIVING RELATIVES:</label>
            <input type="text" id="relatives" name="relatives">
        </div>
        <div class="form-section">
            <label for="relative-address">13. FULL ADDRESS OF RELATIVE:</label>
            <input type="text" id="relative-address" name="relative-address">
        </div>
        <div class="form-section">
            <label for="headman">14. KRAAL HEAD OR HEADMAN:</label>
            <input type="text" id="headman" name="headman">
        </div>
        <div class="form-section">
            <label for="chief">15. CHIEF:</label>
            <input type="text" id="chief" name="chief">
        </div>
        <div class="form-section">
            <label for="clan">16. CLAN:</label>
            <input type="text" id="clan" name="clan">
        </div>
        <div class="form-section">
            <label for="date">Date:</label>
            <input type="text" id="date" name="date">
        </div>
        <div class="form-section">
            <label for="signed">Signed:</label>
            <input type="text" id="signed" name="signed">
        </div>
        <p>I declare that the particulars furnished above are true information relating to my Antecedents.</p>
        <p>Issuing Authority: ____________________________________</p>
        <p>IMMIGRATION AND PASSPORT CONTROL OFFICER</p>
    </div>
</body>
</html>
"""