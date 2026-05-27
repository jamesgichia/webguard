WebGuard — Database Schema Document
Document: Database Schema
Version: 1.0
Status: Draft
Created: May 2026
Author: James Gichia
Repository: docs/technical/database-schema.md

1. Purpose
This document defines the complete relational database schema for WebGuard Version 1.0. It specifies every table, column, data type, constraint, index, and relationship. This document is the direct input to SQLAlchemy model definitions and Alembic migration scripts.

2. Design Principles
UUIDs as primary keys
All primary keys are UUID version 4. This prevents enumeration attacks and is consistent with a security-first product.
UTC timestamps everywhere
All datetime values stored in UTC with timezone awareness. Conversion to local time is the responsibility of the client layer.
Referential integrity enforced at database level
All foreign key relationships enforced with database-level constraints — not just application-level checks.
Sensitive data never stored in plaintext
Passwords stored as bcrypt hashes. API keys stored as SHA-256 hashes. The plaintext value of an API key is never persisted.
Indexes on every foreign key and frequently queried column
Scans queried by user frequently. Findings queried by scan frequently. Indexes ensure these queries remain fast as data grows.

3. Entity Relationship Diagram
#mermaid-r2n0{font-family:inherit;font-size:16px;fill:#E5E5E5;}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#mermaid-r2n0 .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#mermaid-r2n0 .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#mermaid-r2n0 .error-icon{fill:#CC785C;}#mermaid-r2n0 .error-text{fill:#3387a3;stroke:#3387a3;}#mermaid-r2n0 .edge-thickness-normal{stroke-width:1px;}#mermaid-r2n0 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-r2n0 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-r2n0 .edge-thickness-invisible{stroke-width:0;fill:none;}#mermaid-r2n0 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-r2n0 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-r2n0 .marker{fill:#A1A1A1;stroke:#A1A1A1;}#mermaid-r2n0 .marker.cross{stroke:#A1A1A1;}#mermaid-r2n0 svg{font-family:inherit;font-size:16px;}#mermaid-r2n0 p{margin:0;}#mermaid-r2n0 .entityBox{fill:transparent;stroke:#A1A1A1;}#mermaid-r2n0 .relationshipLabelBox{fill:#CC785C;opacity:0.7;background-color:#CC785C;}#mermaid-r2n0 .relationshipLabelBox rect{opacity:0.5;}#mermaid-r2n0 .labelBkg{background-color:rgba(204, 120, 92, 0.5);}#mermaid-r2n0 .edgeLabel{background-color:transparent;}#mermaid-r2n0 .edgeLabel .label rect{fill:transparent;}#mermaid-r2n0 .edgeLabel .label text{fill:#E5E5E5;}#mermaid-r2n0 .edgeLabel .label{fill:#A1A1A1;font-size:14px;}#mermaid-r2n0 .label{font-family:inherit;color:#E5E5E5;}#mermaid-r2n0 .edge-pattern-dashed{stroke-dasharray:8,8;}#mermaid-r2n0 .node rect,#mermaid-r2n0 .node circle,#mermaid-r2n0 .node ellipse,#mermaid-r2n0 .node polygon{fill:transparent;stroke:#A1A1A1;stroke-width:1px;}#mermaid-r2n0 .relationshipLine{stroke:#A1A1A1;stroke-width:1px;fill:none;}#mermaid-r2n0 .marker{fill:none!important;stroke:#A1A1A1!important;stroke-width:1;}#mermaid-r2n0 [data-look=neo].labelBkg{background-color:rgba(204, 120, 92, 0.5);}#mermaid-r2n0 .node .neo-node{stroke:#A1A1A1;}#mermaid-r2n0 [data-look="neo"].node rect,#mermaid-r2n0 [data-look="neo"].cluster rect,#mermaid-r2n0 [data-look="neo"].node polygon{stroke:url(#mermaid-r2n0-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2n0 [data-look="neo"].node path{stroke:url(#mermaid-r2n0-gradient);stroke-width:1px;}#mermaid-r2n0 [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2n0 [data-look="neo"].node .neo-line path{stroke:#A1A1A1;filter:none;}#mermaid-r2n0 [data-look="neo"].node circle{stroke:url(#mermaid-r2n0-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2n0 [data-look="neo"].node circle .state-start{fill:#000000;}#mermaid-r2n0 [data-look="neo"].icon-shape .icon{fill:url(#mermaid-r2n0-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2n0 [data-look="neo"].icon-shape .icon-neo path{stroke:url(#mermaid-r2n0-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2n0 :root{--mermaid-font-family:inherit;}submitsownscontainsscored bygeneratesusersuuididPKvarcharemailvarcharpassword_hashvarcharfull_namebooleanis_activebooleanis_verifiedtimestampcreated_attimestampupdated_attimestamplast_login_atapi_keysuuididPKuuiduser_idFKvarcharkey_hashvarcharkey_prefixvarcharlabelbooleanis_activetimestamplast_used_attimestampcreated_atscansuuididPKuuiduser_idFKvarcharurlvarchardomainvarcharip_addressvarcharprofilevarcharstatusdecimaloverall_scorevarchargradevarcharlabelintegerfindings_countintegercritical_countintegerhigh_countintegermedium_countintegerlow_countintegerinfo_countdecimalduration_secondstexterror_messagetimestampcreated_attimestampupdated_attimestampcompleted_atfindingsuuididPKuuidscan_idFKvarchartitletextdescriptiontextbusiness_impactvarcharseverityvarcharowasp_categoryvarcharowasp_idvarchardimensiontextevidencetextrecommendationvarchareffortjsonbreferencesvarcharfalse_positive_risktimestampcreated_atdimension_scoresuuididPKuuidscan_idFKvarchardimension_namedecimalscoredecimalweightvarchargradeintegerfindings_counttimestampcreated_atreportsuuididPKuuidscan_idFKvarcharformatvarcharfile_pathvarcharfile_nameintegerfile_size_bytestimestampcreated_at

4. Table Specifications
4.1 users
Stores registered user accounts.
sqlCREATE TABLE users (
    id                UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    email             VARCHAR(255)    NOT NULL UNIQUE,
    password_hash     VARCHAR(255)    NOT NULL,
    full_name         VARCHAR(255)    NOT NULL,
    is_active         BOOLEAN         NOT NULL DEFAULT TRUE,
    is_verified       BOOLEAN         NOT NULL DEFAULT FALSE,
    created_at        TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    last_login_at     TIMESTAMPTZ
);
Column descriptions:
ColumnTypeDescriptionidUUIDPrimary key — generated automaticallyemailVARCHAR(255)Unique login identifier — stored lowercasepassword_hashVARCHAR(255)bcrypt hash — minimum 12 roundsfull_nameVARCHAR(255)Display name — shown in dashboardis_activeBOOLEANFalse = account suspended or deletedis_verifiedBOOLEANReserved for future email verificationcreated_atTIMESTAMPTZAccount creation timestamp UTCupdated_atTIMESTAMPTZLast profile update timestamp UTClast_login_atTIMESTAMPTZLast successful login — nullable
Indexes:
sqlCREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_is_active ON users(is_active);
Constraints:

email must be lowercase — enforced at application layer before insert
password_hash must never be empty string
is_active defaults to TRUE — set to FALSE for suspended accounts


4.2 api_keys
Stores API keys for programmatic access. The actual key value is never stored — only a hash and a short prefix for identification.
sqlCREATE TABLE api_keys (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID            NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    key_hash        VARCHAR(64)     NOT NULL UNIQUE,
    key_prefix      VARCHAR(8)      NOT NULL,
    label           VARCHAR(100)    NOT NULL,
    is_active       BOOLEAN         NOT NULL DEFAULT TRUE,
    last_used_at    TIMESTAMPTZ,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);
Column descriptions:
ColumnTypeDescriptionidUUIDPrimary keyuser_idUUIDOwner of this key — cascades on user deletekey_hashVARCHAR(64)SHA-256 hash of the full key — used for lookupkey_prefixVARCHAR(8)First 8 characters of key — shown in UI for identificationlabelVARCHAR(100)User-defined name e.g. "CI Pipeline"is_activeBOOLEANFalse = key revokedlast_used_atTIMESTAMPTZUpdated on every successful usecreated_atTIMESTAMPTZKey creation timestamp UTC
Indexes:
sqlCREATE UNIQUE INDEX idx_api_keys_key_hash ON api_keys(key_hash);
CREATE INDEX idx_api_keys_user_id ON api_keys(user_id);
CREATE INDEX idx_api_keys_is_active ON api_keys(is_active);
Key generation pattern:
Full key:   wg_live_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
Prefix:     wg_live_a (stored in key_prefix — shown in UI)
Hash:       SHA-256(full_key) (stored in key_hash — used for lookup)
Security note:
The full key value is generated once, shown to the user once, and never stored. On subsequent authentication the submitted key is hashed and the hash is compared against stored hashes.
Business rule:
Maximum 5 active API keys per user — enforced at application layer before insert.

4.3 scans
The central table. Every scan ever submitted is a row here.
sqlCREATE TABLE scans (
    id                  UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID            NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    url                 VARCHAR(2048)   NOT NULL,
    domain              VARCHAR(255)    NOT NULL,
    ip_address          VARCHAR(45),
    profile             VARCHAR(20)     NOT NULL CHECK (profile IN ('quick', 'standard', 'deep')),
    status              VARCHAR(20)     NOT NULL CHECK (status IN ('pending', 'running', 'completed', 'failed')),
    overall_score       DECIMAL(3,1),
    grade               VARCHAR(1),
    label               VARCHAR(20),
    findings_count      INTEGER         NOT NULL DEFAULT 0,
    critical_count      INTEGER         NOT NULL DEFAULT 0,
    high_count          INTEGER         NOT NULL DEFAULT 0,
    medium_count        INTEGER         NOT NULL DEFAULT 0,
    low_count           INTEGER         NOT NULL DEFAULT 0,
    info_count          INTEGER         NOT NULL DEFAULT 0,
    duration_seconds    DECIMAL(7,2),
    error_message       TEXT,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    completed_at        TIMESTAMPTZ
);
Column descriptions:
ColumnTypeDescriptionidUUIDPrimary keyuser_idUUIDScan owner — cascades on user deleteurlVARCHAR(2048)Full URL submitted for scanningdomainVARCHAR(255)Extracted domain e.g. example.comip_addressVARCHAR(45)Resolved IP at scan time — IPv6 needs 45 charsprofileVARCHAR(20)quick / standard / deepstatusVARCHAR(20)pending / running / completed / failedoverall_scoreDECIMAL(3,1)0.0 to 10.0 — null until completedgradeVARCHAR(1)A / B / C / D / F — null until completedlabelVARCHAR(20)Excellent / Good / Fair / Poor / Criticalfindings_countINTEGERTotal findings count — denormalized for performancecritical_countINTEGERCritical severity count — denormalizedhigh_countINTEGERHigh severity count — denormalizedmedium_countINTEGERMedium severity count — denormalizedlow_countINTEGERLow severity count — denormalizedinfo_countINTEGERInfo severity count — denormalizedduration_secondsDECIMAL(7,2)Scan duration — null until completederror_messageTEXTError detail if status is failedcreated_atTIMESTAMPTZWhen scan was submittedupdated_atTIMESTAMPTZLast status updatecompleted_atTIMESTAMPTZWhen scan finished — null until completed
Why denormalized counts?
The dashboard and history page display findings counts for every scan in a list. Computing COUNT(*) FROM findings WHERE scan_id = x for 20 scans simultaneously is wasteful. Storing counts directly on the scan row makes list queries fast and simple.
The counts are updated atomically by the Celery worker when the scan completes — not incrementally as findings are inserted.
Indexes:
sqlCREATE INDEX idx_scans_user_id ON scans(user_id);
CREATE INDEX idx_scans_status ON scans(status);
CREATE INDEX idx_scans_user_created ON scans(user_id, created_at DESC);
CREATE INDEX idx_scans_domain ON scans(domain);
The composite index idx_scans_user_created is the most important. The history page query is always WHERE user_id = x ORDER BY created_at DESC LIMIT 20 — this index covers it exactly.

4.4 findings
Every security finding discovered in a scan. One row per finding.
sqlCREATE TABLE findings (
    id                      UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id                 UUID            NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
    title                   VARCHAR(255)    NOT NULL,
    description             TEXT            NOT NULL,
    business_impact         TEXT            NOT NULL,
    severity                VARCHAR(20)     NOT NULL CHECK (severity IN ('critical', 'high', 'medium', 'low', 'info')),
    owasp_category          VARCHAR(100)    NOT NULL,
    owasp_id                VARCHAR(10)     NOT NULL,
    dimension               VARCHAR(50)     NOT NULL,
    evidence                TEXT            NOT NULL,
    recommendation          TEXT            NOT NULL,
    effort                  VARCHAR(20)     NOT NULL CHECK (effort IN ('low', 'medium', 'high')),
    references              JSONB           NOT NULL DEFAULT '[]',
    false_positive_risk     VARCHAR(20)     NOT NULL CHECK (false_positive_risk IN ('low', 'medium', 'high')),
    created_at              TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);
Column descriptions:
ColumnTypeDescriptionidUUIDPrimary keyscan_idUUIDParent scan — cascades on scan deletetitleVARCHAR(255)Short finding title e.g. "Missing Content Security Policy"descriptionTEXTPlain English explanation of what was foundbusiness_impactTEXTWhat this means for the businessseverityVARCHAR(20)critical / high / medium / low / infoowasp_categoryVARCHAR(100)Full category name e.g. "A02:2025 - Security Misconfiguration"owasp_idVARCHAR(10)Short ID e.g. "A02"dimensionVARCHAR(50)Scoring dimension e.g. "header_configuration"evidenceTEXTWhat the scanner observed that produced this findingrecommendationTEXTSpecific actionable remediation stepseffortVARCHAR(20)low / medium / high — estimated fix effortreferencesJSONBArray of reference URLs and CVE IDsfalse_positive_riskVARCHAR(20)How likely this finding is a false positivecreated_atTIMESTAMPTZWhen finding was stored
References JSONB structure:
json[
  {
    "type": "owasp",
    "title": "OWASP CSP Cheat Sheet",
    "url": "https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html"
  },
  {
    "type": "cve",
    "title": "CVE-2021-12345",
    "url": "https://nvd.nist.gov/vuln/detail/CVE-2021-12345",
    "cvss_score": 7.5
  }
]
Indexes:
sqlCREATE INDEX idx_findings_scan_id ON findings(scan_id);
CREATE INDEX idx_findings_scan_severity ON findings(scan_id, severity);
CREATE INDEX idx_findings_severity ON findings(severity);
CREATE INDEX idx_findings_owasp_id ON findings(owasp_id);
CREATE INDEX idx_findings_dimension ON findings(dimension);

4.5 dimension_scores
Stores the six dimension scores for every completed scan. Exactly six rows per completed scan.
sqlCREATE TABLE dimension_scores (
    id                  UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id             UUID            NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
    dimension_name      VARCHAR(50)     NOT NULL,
    score               DECIMAL(3,1)    NOT NULL CHECK (score >= 0.0 AND score <= 10.0),
    weight              DECIMAL(4,3)    NOT NULL,
    grade               VARCHAR(1)      NOT NULL,
    findings_count      INTEGER         NOT NULL DEFAULT 0,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_scan_dimension UNIQUE (scan_id, dimension_name)
);
Column descriptions:
ColumnTypeDescriptionidUUIDPrimary keyscan_idUUIDParent scandimension_nameVARCHAR(50)e.g. transport_security, header_configurationscoreDECIMAL(3,1)0.0 to 10.0weightDECIMAL(4,3)e.g. 0.250 for 25%gradeVARCHAR(1)A / B / C / D / Ffindings_countINTEGERHow many findings in this dimensioncreated_atTIMESTAMPTZWhen score was stored
The unique constraint uq_scan_dimension ensures only one score row per dimension per scan. This prevents duplicate dimension scores from being inserted.
Valid dimension_name values:
transport_security
header_configuration
cookie_security
component_safety
information_exposure
dns_security
Indexes:
sqlCREATE INDEX idx_dimension_scores_scan_id ON dimension_scores(scan_id);

4.6 reports
Stores metadata about generated report files. The actual file content lives on disk or object storage.
sqlCREATE TABLE reports (
    id                  UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id             UUID            NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
    format              VARCHAR(10)     NOT NULL CHECK (format IN ('json', 'html', 'pdf')),
    file_path           VARCHAR(512)    NOT NULL,
    file_name           VARCHAR(255)    NOT NULL,
    file_size_bytes     INTEGER,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_scan_format UNIQUE (scan_id, format)
);
Column descriptions:
ColumnTypeDescriptionidUUIDPrimary keyscan_idUUIDParent scanformatVARCHAR(10)json / html / pdffile_pathVARCHAR(512)Absolute path to file on diskfile_nameVARCHAR(255)e.g. webguard_example.com_20260524.pdffile_size_bytesINTEGERFile size in bytescreated_atTIMESTAMPTZWhen file was generated
The unique constraint uq_scan_format ensures only one report per format per scan.
File naming convention:
webguard_{domain}_{YYYYMMDD}.{format}

Examples:
webguard_example.com_20260524.json
webguard_example.com_20260524.html
webguard_example.com_20260524.pdf
Indexes:
sqlCREATE INDEX idx_reports_scan_id ON reports(scan_id);

5. Complete Schema SQL
The complete schema in execution order — tables created in dependency sequence:
sql-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. Users (no dependencies)
CREATE TABLE users (
    id                UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    email             VARCHAR(255)    NOT NULL UNIQUE,
    password_hash     VARCHAR(255)    NOT NULL,
    full_name         VARCHAR(255)    NOT NULL,
    is_active         BOOLEAN         NOT NULL DEFAULT TRUE,
    is_verified       BOOLEAN         NOT NULL DEFAULT FALSE,
    created_at        TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    last_login_at     TIMESTAMPTZ
);

-- 2. API Keys (depends on users)
CREATE TABLE api_keys (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID            NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    key_hash        VARCHAR(64)     NOT NULL UNIQUE,
    key_prefix      VARCHAR(8)      NOT NULL,
    label           VARCHAR(100)    NOT NULL,
    is_active       BOOLEAN         NOT NULL DEFAULT TRUE,
    last_used_at    TIMESTAMPTZ,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

-- 3. Scans (depends on users)
CREATE TABLE scans (
    id                  UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID            NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    url                 VARCHAR(2048)   NOT NULL,
    domain              VARCHAR(255)    NOT NULL,
    ip_address          VARCHAR(45),
    profile             VARCHAR(20)     NOT NULL CHECK (profile IN ('quick', 'standard', 'deep')),
    status              VARCHAR(20)     NOT NULL CHECK (status IN ('pending', 'running', 'completed', 'failed')),
    overall_score       DECIMAL(3,1),
    grade               VARCHAR(1),
    label               VARCHAR(20),
    findings_count      INTEGER         NOT NULL DEFAULT 0,
    critical_count      INTEGER         NOT NULL DEFAULT 0,
    high_count          INTEGER         NOT NULL DEFAULT 0,
    medium_count        INTEGER         NOT NULL DEFAULT 0,
    low_count           INTEGER         NOT NULL DEFAULT 0,
    info_count          INTEGER         NOT NULL DEFAULT 0,
    duration_seconds    DECIMAL(7,2),
    error_message       TEXT,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    completed_at        TIMESTAMPTZ
);

-- 4. Findings (depends on scans)
CREATE TABLE findings (
    id                      UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id                 UUID            NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
    title                   VARCHAR(255)    NOT NULL,
    description             TEXT            NOT NULL,
    business_impact         TEXT            NOT NULL,
    severity                VARCHAR(20)     NOT NULL CHECK (severity IN ('critical', 'high', 'medium', 'low', 'info')),
    owasp_category          VARCHAR(100)    NOT NULL,
    owasp_id                VARCHAR(10)     NOT NULL,
    dimension               VARCHAR(50)     NOT NULL,
    evidence                TEXT            NOT NULL,
    recommendation          TEXT            NOT NULL,
    effort                  VARCHAR(20)     NOT NULL CHECK (effort IN ('low', 'medium', 'high')),
    references              JSONB           NOT NULL DEFAULT '[]',
    false_positive_risk     VARCHAR(20)     NOT NULL CHECK (false_positive_risk IN ('low', 'medium', 'high')),
    created_at              TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

-- 5. Dimension Scores (depends on scans)
CREATE TABLE dimension_scores (
    id                  UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id             UUID            NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
    dimension_name      VARCHAR(50)     NOT NULL,
    score               DECIMAL(3,1)    NOT NULL CHECK (score >= 0.0 AND score <= 10.0),
    weight              DECIMAL(4,3)    NOT NULL,
    grade               VARCHAR(1)      NOT NULL,
    findings_count      INTEGER         NOT NULL DEFAULT 0,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_scan_dimension UNIQUE (scan_id, dimension_name)
);

-- 6. Reports (depends on scans)
CREATE TABLE reports (
    id                  UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id             UUID            NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
    format              VARCHAR(10)     NOT NULL CHECK (format IN ('json', 'html', 'pdf')),
    file_path           VARCHAR(512)    NOT NULL,
    file_name           VARCHAR(255)    NOT NULL,
    file_size_bytes     INTEGER,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_scan_format UNIQUE (scan_id, format)
);

-- Indexes
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_is_active ON users(is_active);

CREATE UNIQUE INDEX idx_api_keys_key_hash ON api_keys(key_hash);
CREATE INDEX idx_api_keys_user_id ON api_keys(user_id);
CREATE INDEX idx_api_keys_is_active ON api_keys(is_active);

CREATE INDEX idx_scans_user_id ON scans(user_id);
CREATE INDEX idx_scans_status ON scans(status);
CREATE INDEX idx_scans_user_created ON scans(user_id, created_at DESC);
CREATE INDEX idx_scans_domain ON scans(domain);

CREATE INDEX idx_findings_scan_id ON findings(scan_id);
CREATE INDEX idx_findings_scan_severity ON findings(scan_id, severity);
CREATE INDEX idx_findings_severity ON findings(severity);
CREATE INDEX idx_findings_owasp_id ON findings(owasp_id);
CREATE INDEX idx_findings_dimension ON findings(dimension);

CREATE INDEX idx_dimension_scores_scan_id ON dimension_scores(scan_id);

CREATE INDEX idx_reports_scan_id ON reports(scan_id);

6. Common Query Patterns
These are the queries the application will run most frequently. The indexes above are designed specifically for these patterns.
Get user dashboard stats:
sqlSELECT
    COUNT(*) as total_scans,
    AVG(overall_score) as average_score,
    SUM(critical_count) as total_critical,
    SUM(high_count) as total_high,
    SUM(medium_count) as total_medium,
    SUM(low_count) as total_low
FROM scans
WHERE user_id = $1
AND status = 'completed';
Get user scan history (paginated):
sqlSELECT id, url, domain, overall_score, grade, label,
       profile, status, findings_count, created_at
FROM scans
WHERE user_id = $1
ORDER BY created_at DESC
LIMIT 20 OFFSET $2;
Get complete scan result:
sql-- Scan record
SELECT * FROM scans WHERE id = $1 AND user_id = $2;

-- Findings
SELECT * FROM findings
WHERE scan_id = $1
ORDER BY
    CASE severity
        WHEN 'critical' THEN 1
        WHEN 'high' THEN 2
        WHEN 'medium' THEN 3
        WHEN 'low' THEN 4
        WHEN 'info' THEN 5
    END;

-- Dimension scores
SELECT * FROM dimension_scores
WHERE scan_id = $1
ORDER BY weight DESC;
Get score history for chart:
sqlSELECT id, domain, overall_score, grade, created_at
FROM scans
WHERE user_id = $1
AND status = 'completed'
ORDER BY created_at DESC
LIMIT 10;
Authenticate API key:
sqlSELECT ak.*, u.*
FROM api_keys ak
JOIN users u ON u.id = ak.user_id
WHERE ak.key_hash = $1
AND ak.is_active = TRUE
AND u.is_active = TRUE;

7. SQLAlchemy Model Mapping
How the schema maps to Python SQLAlchemy models:
python# api/models/user.py
class User(Base):
    __tablename__ = "users"

    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email         = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name     = Column(String(255), nullable=False)
    is_active     = Column(Boolean, default=True, nullable=False)
    is_verified   = Column(Boolean, default=False, nullable=False)
    created_at    = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at    = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login_at = Column(TIMESTAMP(timezone=True), nullable=True)

    scans    = relationship("Scan", back_populates="user", cascade="all, delete")
    api_keys = relationship("APIKey", back_populates="user", cascade="all, delete")


# api/models/scan.py
class Scan(Base):
    __tablename__ = "scans"

    id               = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id          = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    url              = Column(String(2048), nullable=False)
    domain           = Column(String(255), nullable=False)
    ip_address       = Column(String(45), nullable=True)
    profile          = Column(String(20), nullable=False)
    status           = Column(String(20), nullable=False, default="pending")
    overall_score    = Column(Numeric(3, 1), nullable=True)
    grade            = Column(String(1), nullable=True)
    label            = Column(String(20), nullable=True)
    findings_count   = Column(Integer, default=0, nullable=False)
    critical_count   = Column(Integer, default=0, nullable=False)
    high_count       = Column(Integer, default=0, nullable=False)
    medium_count     = Column(Integer, default=0, nullable=False)
    low_count        = Column(Integer, default=0, nullable=False)
    info_count       = Column(Integer, default=0, nullable=False)
    duration_seconds = Column(Numeric(7, 2), nullable=True)
    error_message    = Column(Text, nullable=True)
    created_at       = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at       = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    completed_at     = Column(TIMESTAMP(timezone=True), nullable=True)

    user             = relationship("User", back_populates="scans")
    findings         = relationship("Finding", back_populates="scan", cascade="all, delete")
    dimension_scores = relationship("DimensionScore", back_populates="scan", cascade="all, delete")
    reports          = relationship("Report", back_populates="scan", cascade="all, delete")

8. Migration Strategy
All schema changes are managed through Alembic migrations.
Initial migration:
bash# Initialize Alembic
alembic init alembic

# Generate initial migration from models
alembic revision --autogenerate -m "initial schema"

# Apply migration
alembic upgrade head
Migration file naming convention:
YYYYMMDD_HHMM_description.py

Examples:
20260524_1430_initial_schema.py
20260601_0900_add_scan_tags.py
Rules:

Never edit a migration that has been applied to production
Every migration must have both upgrade() and downgrade() functions
Test migrations on a copy of production data before applying
Migration scripts are committed to version control alongside model changes


9. Data Lifecycle
On scan submission:
INSERT INTO scans (user_id, url, domain, profile, status)
VALUES ($1, $2, $3, $4, 'pending')
On scan start (worker picks up job):
UPDATE scans SET status = 'running', updated_at = NOW()
WHERE id = $1
On scan completion (worker stores results):
-- Insert findings (batch insert)
INSERT INTO findings (...) VALUES (...), (...), (...)

-- Insert dimension scores (6 rows)
INSERT INTO dimension_scores (...) VALUES (...), (...), (...)

-- Insert report metadata
INSERT INTO reports (...) VALUES (...)

-- Update scan with results
UPDATE scans SET
    status = 'completed',
    overall_score = $1,
    grade = $2,
    label = $3,
    findings_count = $4,
    critical_count = $5,
    high_count = $6,
    medium_count = $7,
    low_count = $8,
    info_count = $9,
    duration_seconds = $10,
    completed_at = NOW(),
    updated_at = NOW()
WHERE id = $11
On scan failure:
UPDATE scans SET
    status = 'failed',
    error_message = $1,
    updated_at = NOW()
WHERE id = $2
On user account deletion:
-- CASCADE handles everything automatically
DELETE FROM users WHERE id = $1
-- Automatically deletes: api_keys, scans,
-- findings, dimension_scores, reports

This document is version controlled. Schema changes require a new Alembic migration and an update to this document. Changes must be committed together.
Last updated: May 2026
