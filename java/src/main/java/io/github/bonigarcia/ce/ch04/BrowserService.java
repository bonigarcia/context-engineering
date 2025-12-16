/*
 * (C) Copyright 2025 Boni Garcia (https://bonigarcia.github.io/)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */
package io.github.bonigarcia.ce.ch04;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;

public class BrowserService {

    private WebDriver driver;

    public synchronized String startBrowser(String browserName) {
        try {
            if (driver != null) {
                return "Browser is already running. Please close it first.";
            }
            if (browserName.equalsIgnoreCase("chrome")) {
                driver = new ChromeDriver();
            } else if (browserName.equalsIgnoreCase("firefox")) {
                driver = new FirefoxDriver();
            } else {
                return "Unsupported browser: " + browserName;
            }
            return "Browser started successfully";
        } catch (Exception e) {
            return "Error starting browser: " + e.getMessage();
        }
    }

    public synchronized String navigate(String url) {
        if (driver == null) {
            return "Browser not started. Please start a browser first.";
        }
        try {
            driver.get(url);
            return "Navigation successful";
        } catch (Exception e) {
            return "Error navigating to url: " + e.getMessage();
        }
    }

    public synchronized String closeBrowser() {
        if (driver == null) {
            return "Browser not started.";
        }
        String status;
        try {
            driver.quit();
            status = "Browser closed successfully";
        } catch (Exception e) {
            status = "Error closing browser: " + e.getMessage();
        }
        driver = null;
        return status;
    }

}
