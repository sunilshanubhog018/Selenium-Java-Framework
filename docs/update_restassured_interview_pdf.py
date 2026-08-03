"""Rebuild Rest Assured Interview Q&A PDF with accuracy polish."""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Preformatted
)

OUT = Path(
    r"C:\Users\sunil\OneDrive\Desktop\Java_selenium_material"
    r"\CLAUDE AI NOTES\REST ASSURED API AUTOAMTION NOTES"
    r"\Rest_Assured_Interview_Questions_Answers_grokbuild.pdf"
)

NAVY = HexColor("#0b3d5c")
TEAL = HexColor("#0f766e")
GREEN = HexColor("#166534")
LIGHT = HexColor("#f0f9ff")
SOFT = HexColor("#e2e8f0")
DARK = HexColor("#1e293b")
MUTED = HexColor("#475569")
GOLD = HexColor("#b45309")
RED = HexColor("#9f1239")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TMain", fontName="Helvetica-Bold", fontSize=14.5,
                          leading=18, textColor=white, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="TSub", fontName="Helvetica", fontSize=8.8,
                          leading=11.5, textColor=HexColor("#dbeafe"), alignment=TA_CENTER))
styles.add(ParagraphStyle(name="DH1", fontName="Helvetica-Bold", fontSize=10.5,
                          leading=13, textColor=NAVY, spaceBefore=6, spaceAfter=2))
styles.add(ParagraphStyle(name="DH2", fontName="Helvetica-Bold", fontSize=9,
                          leading=11, textColor=TEAL, spaceBefore=4, spaceAfter=2))
styles.add(ParagraphStyle(name="DQ", fontName="Helvetica-Bold", fontSize=8.2,
                          leading=10.4, textColor=NAVY, spaceBefore=3, spaceAfter=1))
styles.add(ParagraphStyle(name="DA", fontName="Helvetica", fontSize=7.8,
                          leading=9.9, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=1))
styles.add(ParagraphStyle(name="DTip", fontName="Helvetica-Oblique", fontSize=7.1,
                          leading=9, textColor=GOLD, leftIndent=3, spaceAfter=1))
styles.add(ParagraphStyle(name="DFix", fontName="Helvetica-Oblique", fontSize=7.0,
                          leading=8.9, textColor=GREEN, spaceAfter=2))
styles.add(ParagraphStyle(name="DBody", fontName="Helvetica", fontSize=7.9,
                          leading=10, textColor=DARK, spaceAfter=2))
styles.add(ParagraphStyle(name="CodeB", fontName="Courier", fontSize=6.1,
                          leading=7.8, textColor=DARK, backColor=LIGHT, spaceBefore=1, spaceAfter=1))
styles.add(ParagraphStyle(name="DCell", fontName="Helvetica", fontSize=6.7,
                          leading=8.4, textColor=DARK))
styles.add(ParagraphStyle(name="DHead", fontName="Helvetica-Bold", fontSize=6.7,
                          leading=8.4, textColor=white))
styles.add(ParagraphStyle(name="LvlB", fontName="Helvetica-Bold", fontSize=7.2,
                          textColor=HexColor("#1d4ed8"), spaceAfter=1))
styles.add(ParagraphStyle(name="LvlM", fontName="Helvetica-Bold", fontSize=7.2,
                          textColor=TEAL, spaceAfter=1))
styles.add(ParagraphStyle(name="LvlR", fontName="Helvetica-Bold", fontSize=7.2,
                          textColor=RED, spaceAfter=1))


def P(t, s="DA"):
    return Paragraph(t, styles[s])


def code(t):
    return Preformatted(t.rstrip(), styles["CodeB"])


def tip(t):
    return P(f"<b>Tip:</b> {t}", "DTip")


def hline():
    return HRFlowable(width="100%", thickness=0.35, color=SOFT, spaceBefore=1, spaceAfter=2)


def qa(n, q, parts):
    items = [P(f"Q{n}. {q}", "DQ")]
    for p in parts:
        items.append(P(p, "DA") if isinstance(p, str) else p)
    return KeepTogether(items)


def footer(canvas, doc):
    canvas.saveState()
    page = canvas.getPageNumber()
    if page > 1:
        canvas.setFillColor(NAVY)
        canvas.rect(0, A4[1] - 12, A4[0], 12, fill=1, stroke=0)
        canvas.setFillColor(white)
        canvas.setFont("Helvetica", 6.4)
        canvas.drawString(26, A4[1] - 8, "Rest Assured API Automation | Interview Q&A")
        canvas.drawRightString(A4[0] - 26, A4[1] - 8, "Easy · Medium · Difficult")
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 6.4)
        canvas.drawCentredString(A4[0] / 2, 10, f"Page {page}")
    canvas.restoreState()


def build():
    story = []

    cover = Table([
        [P("Rest Assured API Automation", "TMain")],
        [P("Interview Questions &amp; Answers<br/>"
           "Easy · Medium · Difficult / Real-World · Banking scenarios<br/><br/>"
           "45 Q&amp;A · Practical code patterns · Framework design thinking",
           "TSub")],
    ], colWidths=[6.7 * inch])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 18),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(Spacer(1, 30))
    story.append(cover)
    story.append(Spacer(1, 8))
    story.append(P(
        "Original guide was already strong. Verified and lightly polished for interview accuracy "
        "(auth, specs, parallel, security, banking).",
        "DBody"
    ))
    story.append(P(
        "Polish: global baseURI vs RequestSpec; preemptive basic auth; schema dependency; "
        "HTTP vs business status; idempotency; log redaction; parallel data isolation.",
        "DFix"
    ))
    story.append(P("How to use: answer first, then read. Practice every coding snippet in IDE.", "DBody"))
    story.append(PageBreak())

    # EASY
    story.append(P("SECTION 1 — EASY LEVEL", "DH1"))
    story.append(P("Fundamentals &amp; syntax — short, crisp answers", "LvlB"))
    story.append(hline())

    story.append(qa(1, "What is Rest Assured?", [
        "Java library to automate REST APIs with a fluent BDD-style given/when/then API for requests and validations "
        "(status, headers, body, cookies, time).",
    ]))
    story.append(qa(2, "Why Rest Assured?", [
        "Readable Java DSL, JSON/XML support, TestNG/JUnit friendly, POJO (de)serialization, auth helpers, "
        "schema validation modules, easy CI integration.",
    ]))
    story.append(qa(3, "Basic structure?", [
        "<b>given()</b> preconditions (headers, params, body, auth) → <b>when()</b> HTTP verb → "
        "<b>then()</b> assertions.",
    ]))
    story.append(qa(4, "Simple GET?", [
        code('given()\n.when()\n  .get("https://api.example.com/users/1")\n.then()\n  .statusCode(200);'),
    ]))
    story.append(qa(5, "Validate status code?", [
        ".then().statusCode(200) or .assertThat().statusCode(equalTo(200)).",
    ]))
    story.append(qa(6, "Print response body?", [
        ".then().log().body() or response.getBody().asString() after extract/response object.",
    ]))
    story.append(qa(7, "GET vs POST?", [
        "GET retrieves (should be safe/idempotent by REST design; typically no body). "
        "POST submits/creates; usually has body; may create resources. (Note: real APIs sometimes misuse verbs.)",
    ]))
    story.append(qa(8, "Query params?", [
        code('given().queryParam("page", 1).queryParam("size", 20)\n.when().get("/users");'),
    ]))
    story.append(qa(9, "Path params?", [
        code('given().pathParam("id", 10)\n.when().get("/users/{id}");'),
    ]))
    story.append(qa(10, "Headers?", [
        ".header(\"Content-Type\", \"application/json\") or .headers(map).",
    ]))
    story.append(qa(11, "JSON body in POST?", [
        code('given()\n  .contentType(ContentType.JSON)\n  .body(jsonStringOrMapOrPojo)\n'
             ".when().post(\"/users\");"),
    ]))
    story.append(qa(12, "Content-Type vs Accept?", [
        "Content-Type = format of request body. Accept = preferred response format.",
    ]))
    story.append(qa(13, "Extract JSON value?", [
        code('String name = response.jsonPath().getString("data.name");\n'
             '// or fluent:\n.then().body("data.name", equalTo("John"));'),
    ]))
    story.append(qa(14, "Hamcrest?", [
        "Matcher library used in assertions: equalTo, hasItem, notNullValue, greaterThan, hasSize, etc.",
    ]))
    story.append(qa(15, "Log request/response?", [
        "given().log().all() and then().log().all(); also .log().ifValidationFails() to reduce noise.",
    ]))

    story.append(PageBreak())

    # MEDIUM
    story.append(P("SECTION 2 — MEDIUM LEVEL", "DH1"))
    story.append(P("POJOs, auth, specs, schema, data-driven", "LvlM"))
    story.append(hline())

    story.append(qa("M1", "given/when/then real example?", [
        code('given()\n  .baseUri("https://reqres.in")\n  .contentType(ContentType.JSON)\n'
             '  .body("{\\"name\\":\\"morpheus\\",\\"job\\":\\"leader\\"}")\n'
             ".when().post(\"/api/users\")\n"
             ".then().statusCode(201).body(\"name\", equalTo(\"morpheus\"));"),
    ]))
    story.append(qa("M2", "Nested JSON fields?", [
        ".body(\"data.user.address.city\", equalTo(\"London\")). Arrays: data[0].id ; "
        "Groovy finders where enabled: data.findAll { it.active }.name",
    ]))
    story.append(qa("M3", "JSON array size?", [
        ".body(\"data.size()\", equalTo(6)) or .body(\"data\", hasSize(6)).",
    ]))
    story.append(qa("M4", "Serialization / deserialization?", [
        "POJO→JSON for request (.body(pojo)); JSON→POJO via response.as(User.class). Needs Jackson/Gson on classpath.",
    ]))
    story.append(qa("M5", "POJO usage?", [
        "Fields + getters/setters (or Lombok). Send .body(user); read User u = response.as(User.class).",
    ]))
    story.append(qa("M6", "Basic Authentication?", [
        code('given().auth().preemptive().basic("user", "pass")\n'
             "// preemptive: send credentials before 401 challenge\n"
             "// .auth().basic(...) waits for challenge (challenge-based)"),
    ]))
    story.append(qa("M7", "Bearer / OAuth2 token?", [
        code('given().auth().oauth2(token)\n// or\n.header("Authorization", "Bearer " + token)'),
        tip("Never hardcode tokens — env vars / CI secrets / vault."),
    ]))
    story.append(qa("M8", "baseURI / basePath?", [
        "RestAssured.baseURI/basePath are global statics (simple demos). Prefer RequestSpecification for frameworks "
        "and parallel safety.",
        code('RequestSpecification req = new RequestSpecBuilder()\n'
             '  .setBaseUri(config.get("base.uri"))\n'
             '  .setContentType(ContentType.JSON)\n'
             '  .build();\n'
             'given().spec(req).when().get("/accounts");'),
    ]))
    story.append(qa("M9", "RequestSpecification & ResponseSpecification?", [
        "Reuse common request setup (URI, headers, auth) and common response expectations (status, content-type). "
        "Keeps tests DRY.",
    ]))
    story.append(qa("M10", "Validate response time?", [
        ".then().time(lessThan(2000L)) // ms — smoke SLA only, not full load testing.",
    ]))
    story.append(qa("M11", "JSON schema validation?", [
        "Dependency: io.rest-assured:json-schema-validator. "
        ".then().body(matchesJsonSchemaInClasspath(\"schemas/user.json\")).",
    ]))
    story.append(qa("M12", "Multipart file upload?", [
        code('given().multiPart("file", new File("data.csv"))\n'
             '  .multiPart("type", "KYC")\n'
             ".when().post(\"/upload\");"),
    ]))
    story.append(qa("M13", "Cookies reuse?", [
        "Map cookies = response.getCookies(); next call .cookies(cookies) or .cookie(\"JSESSIONID\", val).",
    ]))
    story.append(qa("M14", "extract().path vs jsonPath().get?", [
        "Both read JSON paths. extract().path in fluent chain; jsonPath() on stored Response. Similar for JSON.",
    ]))
    story.append(qa("M15", "Data-driven with TestNG?", [
        "@DataProvider or Excel/JSON rows feed endpoint, payload, expected status/body into one @Test template.",
    ]))

    story.append(PageBreak())

    # DIFFICULT
    story.append(P("SECTION 3 — DIFFICULT / REAL-WORLD", "DH1"))
    story.append(P("Framework · security · banking · parallel", "LvlR"))
    story.append(hline())

    story.append(qa("D1", "Design scalable Rest Assured banking framework?", [
        "Config (env + secrets) → Request/Response specs → service clients (AccountAPI, TransferAPI) → "
        "POJO/builders → thin TestNG tests (smoke/regression) → token manager → optional DB asserts → "
        "Allure/Extent + CI. Never commit PAN/PII/tokens.",
    ]))
    story.append(qa("D2", "Dynamic token expiry?", [
        "TokenManager caches token + expiry; refresh on expiry or 401; thread-safe per user/role; "
        "inject via filter/spec. Don’t login every test unless testing login.",
    ]))
    story.append(qa("D3", "HTTP 200 but business FAILED?", [
        "Assert both layers: statusCode(200).body(\"status\", equalTo(\"SUCCESS\")). "
        "HTTP success ≠ business success.",
    ]))
    story.append(qa("D4", "Idempotency PUT/DELETE/payment?", [
        "Replay same request with same Idempotency-Key; assert no double side-effect via GET balance/ledger count.",
    ]))
    story.append(qa("D5", "Chain create→get→update→delete?", [
        "Extract id from create; pass through; cleanup in @AfterMethod even on failure. Plus isolated atomic tests.",
    ]))
    story.append(qa("D6", "Flaky async / eventual consistency?", [
        "Poll GET until COMPLETED with timeout/interval — not fixed sleep. Separate env flakes from product bugs.",
    ]))
    story.append(qa("D7", "Mask tokens/account numbers in logs?", [
        "Custom Filter redacts Authorization and sensitive JSON fields; limit body logging in CI; synthetic data.",
    ]))
    story.append(qa("D8", "Rest Assured vs Postman vs Karate?", [
        "Rest Assured: Java code, reuse, complex logic. Postman: exploration/collections. Karate: DSL+Gherkin style. "
        "Choose by team language and complexity.",
    ]))
    story.append(qa("D9", "Signature / encryption headers?", [
        "Compute HMAC/RSA in util from vault secret; never log keys; unit-test crypto separate from E2E API flow.",
    ]))
    story.append(qa("D10", "Contract testing?", [
        "JSON Schema in CI; optional Pact/Spring Cloud Contract; version APIs; assert required fields/types/enums.",
    ]))
    story.append(qa("D11", "401 vs 403 vs 404 vs 429?", [
        "401 unauthenticated; 403 authenticated but forbidden; 404 missing resource; 429 rate limit "
        "(Retry-After if present). Don’t DOS shared envs in CI.",
    ]))
    story.append(qa("D12", "Parallel Rest Assured safely?", [
        "No mutable static specs state; unique data per thread (UUID); tokens per role/thread; "
        "connection limits so suite doesn’t overwhelm API.",
    ]))
    story.append(qa("D13", "Payment API slow only in UAT?", [
        "Measure .time() + correlation-id; env-specific SLA thresholds; don’t only increase sleep; "
        "classify env capacity vs product regression.",
    ]))
    story.append(qa("D14", "DB validation with API tests?", [
        "After call, JDBC assert persistence; or follow-up GET if DB closed; Testcontainers in lower envs.",
    ]))
    story.append(qa("D15", "Banking bug API tests catch?", [
        "Double debit on retry without idempotency key — two transfers same key → one ledger entry + correct balance.",
    ]))

    story.append(Spacer(1, 6))
    story.append(P("SECTION 4 — QUICK INTERVIEW TIPS", "DH1"))
    story.append(hline())
    for t in [
        "Explain WHY, not only syntax.",
        "Coding round order: given/when/then → specs → POJO → token → data-driven.",
        "Banking: security, PII masking, idempotency, roles, audit/correlation ids.",
        "Be honest about tools you actually used.",
        "Prepare one framework diagram + one E2E create→get→delete story.",
    ]:
        story.append(P(f"• {t}", "DBody"))

    story.append(P("60-second pitch", "DH2"))
    story.append(P(
        "“I build Rest Assured + TestNG suites with env config, reusable RequestSpecifications, service clients, "
        "POJO payloads, token manager, schema checks on critical contracts, data-driven regression, Allure/CI parallel "
        "runs. Assertions cover HTTP and business status; sensitive fields are redacted in logs.”",
        "DTip"
    ))

    story.append(P("Must-practice snippets", "DH2"))
    story.append(P(
        "1) GET + status + body  2) POST POJO + extract id  3) Bearer header  4) path+query params  "
        "5) RequestSpec reuse  6) JsonPath list  7) Schema validation  8) create→get→delete cleanup",
        "DBody"
    ))

    story.append(Spacer(1, 6))
    story.append(hline())
    story.append(P("End of Rest Assured Interview Q&amp;A — verified &amp; polished. Good luck!", "DBody"))

    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=28, rightMargin=28, topMargin=24, bottomMargin=22,
        title="Rest Assured Interview Q&A",
        author="API Automation Interview Prep",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("Updated:", OUT, "bytes=", OUT.stat().st_size)


if __name__ == "__main__":
    build()
