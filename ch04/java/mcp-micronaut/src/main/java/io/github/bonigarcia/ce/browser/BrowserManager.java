/*
 * (C) Copyright 2026 Boni Garcia (https://bonigarcia.github.io/)
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
package io.github.bonigarcia.ce.browser;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;

public class BrowserManager {

    private WebDriver driver;

    public BrowserResult start(String browserName) {
        if (driver != null) {
            return BrowserResult.error("Browser is already open.");
        }
        try {
            BrowserType type = BrowserType.from(browserName);
            switch (type) {
            case CHROME -> driver = new ChromeDriver();
            case FIREFOX -> driver = new FirefoxDriver();
            }
            return BrowserResult.ok("Browser started successfully.");
        } catch (IllegalArgumentException e) {
            return BrowserResult.error("Unsupported browser: " + browserName);
        } catch (Exception e) {
            return BrowserResult
                    .error("Error starting browser: " + e.getMessage());
        }
    }

    public BrowserResult navigate(String url) {
        if (driver == null) {
            return BrowserResult.error("Browser not started.");
        }
        try {
            driver.get(url);
            return BrowserResult.ok("Navigation successful.");
        } catch (Exception e) {
            return BrowserResult.error("Error navigating: " + e.getMessage());
        }
    }

    public BrowserResult close() {
        if (driver == null) {
            return BrowserResult.error("Browser not started.");
        }
        try {
            driver.quit();
            return BrowserResult.ok("Browser closed successfully.");
        } catch (Exception e) {
            return BrowserResult
                    .error("Error closing browser: " + e.getMessage());
        } finally {
            driver = null;
        }
    }

    public BrowserResult readText() {
        if (driver == null) {
            return BrowserResult.error("Browser not started.");
        }
        try {
            String text = driver.findElement(By.tagName("body")).getText();
            return BrowserResult.ok(text);
        } catch (Exception e) {
            return BrowserResult.error("Error reading page: " + e.getMessage());
        }
    }
}
