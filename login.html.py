<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Classic Collection - Login</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }

        body {
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #f5f2ed;
            padding: 20px;
        }

        .container {
            width: 900px;
            min-height: 550px;
            display: flex;
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        }

        /* LEFT SIDE */

        .left {
            width: 50%;
            background: #171717;
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 60px;
        }

        .logo {
            font-size: 32px;
            letter-spacing: 5px;
            font-weight: bold;
            margin-bottom: 15px;
        }

        .logo span {
            color: #b08d57;
        }

        .left h2 {
            font-size: 42px;
            margin-bottom: 20px;
        }

        .left p {
            color: #cccccc;
            line-height: 1.7;
            font-size: 16px;
            max-width: 350px;
        }

        .line {
            width: 70px;
            height: 3px;
            background: #b08d57;
            margin: 20px 0;
        }

        /* RIGHT SIDE */

        .right {
            width: 50%;
            padding: 55px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .right h1 {
            font-size: 32px;
            color: #171717;
            margin-bottom: 8px;
        }

        .subtitle {
            color: #777;
            margin-bottom: 30px;
            font-size: 14px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: bold;
            font-size: 14px;
        }

        .input-box {
            position: relative;
            margin-bottom: 20px;
        }

        input {
            width: 100%;
            padding: 14px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 15px;
            transition: 0.3s;
        }

        input:focus {
            outline: none;
            border-color: #b08d57;
            box-shadow: 0 0 5px rgba(176, 141, 87, 0.2);
        }

        .password-input {
            padding-right: 45px;
        }

        .show-password {
            position: absolute;
            right: 14px;
            top: 14px;
            cursor: pointer;
            color: #777;
            font-size: 16px;
        }

        .forgot {
            text-align: right;
            margin-top: -8px;
            margin-bottom: 25px;
        }

        .forgot a {
            color: #9b743e;
            text-decoration: none;
            font-size: 14px;
        }

        .forgot a:hover {
            text-decoration: underline;
        }

        .login-btn {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 8px;
            background: #b08d57;
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }

        .login-btn:hover {
            background: #96733f;
            transform: translateY(-1px);
        }

        .register {
            text-align: center;
            margin-top: 25px;
            color: #777;
            font-size: 14px;
        }

        .register a {
            color: #9b743e;
            font-weight: bold;
            text-decoration: none;
        }

        .register a:hover {
            text-decoration: underline;
        }

        .message {
            margin-top: 15px;
            text-align: center;
            font-size: 14px;
            font-weight: bold;
            display: none;
        }

        /* MOBILE */

        @media (max-width: 700px) {

            .container {
                width: 100%;
                min-height: auto;
            }

            .left {
                display: none;
            }

            .right {
                width: 100%;
                padding: 40px 30px;
            }
        }
    </style>
</head>

<body>

    <div class="container">

        <!-- LEFT SIDE -->

        <div class="left">

            <div class="logo">
                CLASSIC <span>COLLECTION</span>
            </div>

            <div class="line"></div>

            <h2>Fashion<br>For Everyone</h2>

            <p>
                Timeless styles. Modern fashion.
                Discover clothing designed for
                every occasion.
            </p>

        </div>


        <!-- RIGHT SIDE -->

        <div class="right">

            <h1>Welcome Back!</h1>

            <p class="subtitle">
                Login to your Classic Collection account
            </p>


            <form id="loginForm">

                <!-- USERNAME -->

                <label for="username">
                    Email / Username
                </label>

                <div class="input-box">

                    <input
                        type="text"
                        id="username"
                        placeholder="Enter your email or username"
                    >

                </div>


                <!-- PASSWORD -->

                <label for="password">
                    Password
                </label>

                <div class="input-box">

                    <input
                        type="password"
                        id="password"
                        class="password-input"
                        placeholder="Enter your password"
                    >

                    <span
                        class="show-password"
                        onclick="togglePassword()"
                        id="eye"
                    >
                        👁
                    </span>

                </div>


                <!-- FORGOT PASSWORD -->

                <div class="forgot">

                    <a href="#">
                        Forgot Password?
                    </a>

                </div>


                <!-- LOGIN BUTTON -->

                <button
                    type="submit"
                    class="login-btn"
                >
                    LOGIN
                </button>

            </form>


            <!-- MESSAGE -->

            <div
                class="message"
                id="message"
            ></div>


            <!-- REGISTER -->

            <div class="register">

                Don't have an account?

                <a href="#">
                    Create Account
                </a>

            </div>

        </div>

    </div>


    <!-- JAVASCRIPT -->

    <script>

        function togglePassword() {

            const password =
                document.getElementById("password");

            const eye =
                document.getElementById("eye");

            if (password.type === "password") {

                password.type = "text";
                eye.innerHTML = "🙈";

            } else {

                password.type = "password";
                eye.innerHTML = "👁";

            }
        }


        document
            .getElementById("loginForm")
            .addEventListener("submit", function(event) {

                event.preventDefault();

                const username =
                    document.getElementById("username").value.trim();

                const password =
                    document.getElementById("password").value.trim();

                const message =
                    document.getElementById("message");


                if (username === "" || password === "") {

                    message.style.display = "block";
                    message.style.color = "red";
                    message.innerHTML =
                        "Please enter username and password.";

                    return;
                }


                message.style.display = "block";
                message.style.color = "green";
                message.innerHTML =
                    "Login successful!";

            });

    </script>

</body>
</html>
