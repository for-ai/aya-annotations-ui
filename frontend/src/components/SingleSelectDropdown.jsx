import React from "react";
import Select from "react-select";

function SingleSelectDropdown(props) {
  const optionsListed = props.options.map((option) => ({
    value: option.id,
    label: option.name,
    code: option.code,
  }));

  let currentValue;
  if (props.entity === "Age Range" && props.currentValue) {
    const ageRangeCode = `${props.currentValue[0]}-${props.currentValue[1]}`;
    currentValue = optionsListed.find((option) => option.code === ageRangeCode);
  } else {
    currentValue = optionsListed.find(
      (option) => option.value === props.currentValue
    );
  }

  return (
    <Select
      className="basic-single w-full"
      classNamePrefix="select"
      defaultValue={currentValue}
      isSearchable={true}
      isClearable={true}
      name={props.entity}
      placeholder={`Select ${props.entity}`}
      options={optionsListed}
      onChange={props.onChange}
    />
  );
}

export default SingleSelectDropdown;
