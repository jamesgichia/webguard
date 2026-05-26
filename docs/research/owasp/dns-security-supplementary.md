Additional WebGuard Notes — DNS Security Research
File: docs/research/owasp/dns-security-supplementary.md
Since WebGuard includes DNS security as a scoring dimension not directly mapped to a single OWASP category, documenting the DNS checks separately ensures completeness.
DNS checks and their OWASP mappings:
CheckMaps ToSeverityMissing SPF recordA02 Security MisconfigurationMediumPermissive SPF (+all)A02 Security MisconfigurationHighMissing DMARCA02 Security MisconfigurationMediumDMARC p=noneA02 Security MisconfigurationLowMissing DNSSECA04 Cryptographic FailuresLowMissing CAA recordsA04 Cryptographic FailuresLow

