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

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;

public class BrowserService {

    private WebDriver driver;

    private static final String BROWSER_NOT_STARTED = "Browser not started. Please start a browser first.";
    private static final String BROWSER_STARTED = "Browser started successfully.";

    public synchronized String startBrowser(String browserName) {
        String response;
        try {
            if (driver != null) {
                response = "Browser is already running. Please close it first.";
            } else if (browserName.equalsIgnoreCase("chrome")) {
                driver = new ChromeDriver();
                response = BROWSER_STARTED;
            } else if (browserName.equalsIgnoreCase("firefox")) {
                driver = new FirefoxDriver();
                response = BROWSER_STARTED;
            } else {
                response = "Error unsupported browser: " + browserName;
            }

        } catch (Exception e) {
            response = "Error starting browser: " + e.getMessage();
        }
        return response;
    }

    public synchronized String navigate(String url) {
        String response;
        if (driver == null) {
            response = BROWSER_NOT_STARTED;
        } else {
            try {
                driver.get(url);
                response = "Navigation successful.";
            } catch (Exception e) {
                response = "Error navigating to url: " + e.getMessage();
            }
        }
        return response;
    }

    public synchronized String closeBrowser() {
        String response;
        if (driver == null) {
            response = BROWSER_NOT_STARTED;
        } else {
            try {
                driver.quit();
                response = "Browser closed successfully.";
            } catch (Exception e) {
                response = "Error closing browser: " + e.getMessage();
            }
        }
        driver = null;
        return response;
    }

    public synchronized String readPageText() {
        String response;
        if (driver == null) {
            response = BROWSER_NOT_STARTED;
        } else {
            try {
                response = driver.findElement(By.tagName("body")).getText();
            } catch (Exception e) {
                response = "Error reading page text: " + e.getMessage();
            }
        }
        return response;
    }

}
