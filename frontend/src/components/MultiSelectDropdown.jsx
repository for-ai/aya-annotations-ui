import React from "react";
import Select from "react-select";

function MultiSelectDropdown(props) {
  const optionsListed = props.options.map((option) => ({
    value: option.id,
    label: option.name,
    code: option.code,
    charCode: option.character_code,
  }));

  const currentValues = optionsListed.filter(
    (option) =>
      props.currentValues && props.currentValues.includes(option.value)
  );

  const formatOptionLabel = ({ label, charCode }) => (
    <div>
      <span>{label}</span>
      <span style={{ color: "gray", marginLeft: "0.5em" }}>({charCode})</span>
    </div>
  );

  return (
    <Select
      defaultValue={currentValues}
      isMulti
      name={props.entity}
      placeholder={`Select ${props.entity}`}
      options={optionsListed}
      className="basic-multi-select w-full"
      classNamePrefix="select"
      onChange={props.onChange}
      formatOptionLabel={formatOptionLabel}
    />
  );
}

export default MultiSelectDropdown;
