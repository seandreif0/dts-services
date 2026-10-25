# dts-services

Small internal services run by the Digital Technology Services (DTS) team. Each lives under `services/<name>/` and is deployed to on-prem VMs today.

| Service | Purpose |
|---|---|
| badge-access | Building badge lookup |
| desk-booking | Hot-desk availability |
| expense-lookup | Read-only expense claim status |
| training-catalog | Internal training courses |
| it-asset-inventory | Laptop and monitor assignments |
| visitor-register | Front-desk visitor log |

Run one service's tests:

```sh
cd services/<name>
pip install -r requirements.txt
pytest
```

Run all tests: `make test`. See `MIGRATION.md` for the cloud migration plan.
