import React from "react";

const BRANDS = ["Trek", "Shimano", "SRAM"];

export default function CompanySelector({ company, setCompany }) {
  return (
    <div className="company-selector">
      <p className="ui-meta">Documentation source</p>

      <div className="brand-segment">
        {BRANDS.map((b) => (
          <button
            key={b}
            className={`segment-btn ${company === b ? "active" : ""}`}
            onClick={() => setCompany(b)}
          >
            {b}
          </button>
        ))}
      </div>
    </div>
  );
}
