import React from "react";
import CreatableSelect from "react-select/creatable";

const NoDropdownIndicator = (props) => {
  return null;
};

const DialectInput = ({ dialects, setDialects }) => {
  const handleChange = (values) => {
    const newDialects = values ? values.map((value) => value.label) : [];
    setDialects(newDialects);
  };

  const handleMenuOpen = () => false; // Prevent menu from opening

  const formattedDialects = dialects.map((dialect) => ({
    label: dialect,
    value: dialect,
  }));

  return (
    <CreatableSelect
      isMulti
      className="w-full"
      value={formattedDialects}
      onChange={handleChange}
      placeholder="Add a dialect..."
      components={{
        DropdownIndicator: NoDropdownIndicator,
        IndicatorSeparator: () => null,
      }} // Remove dropdown indicator
      onMenuOpen={handleMenuOpen}
      noOptionsMessage={() => "Type to add a dialect"}
    />
  );
};

export default DialectInput;
