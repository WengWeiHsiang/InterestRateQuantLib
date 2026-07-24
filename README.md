# InterestRateQuantLib

Enterprise Interest Rate Quantitative Library based on *Brigo & Mercurio (2nd Edition)* with Multi-Curve & RFR (SOFR/€STR/SONIA) Support.

## Architecture Highlights
- **Market Layer**: Decoupled Data Providers & Fixing Managers.
- **Index-Driven Design**: All instruments depend on `InterestRateIndex` (USD LIBOR, SOFR, EURIBOR).
- **Multi-Curve Framework**: Independent Discount & Projection Curve dynamics.
- **Full Model Matrix**: HW, G2++, BK, CIR, LMM, HJM, SABR.

## Quick Start
```bash
pip install -e .[dev]
pytest
```