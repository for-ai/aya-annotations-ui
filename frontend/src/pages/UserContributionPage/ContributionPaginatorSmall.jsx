import React from "react";
import { Box } from "@chakra-ui/react";
import Select from "react-select";

const ContributionPaginatorSmall = ({
  contributions,
  selectedContribution,
  setSelectedContribution,
  currentPages,
  setCurrentPages,
  activeTaskType,
  pageOptions,
}) => {
  const handlePageChange = (selectedPage) => {
    setCurrentPages((prevPages) => ({
      ...prevPages,
      [activeTaskType]: selectedPage,
    }));
  };

  return (
    <Box mt={4}>
      <Select
        classNamePrefix="select"
        isSearchable={true}
        isClearable={false}
        name="Contribution"
        defaultValue={
          contributions[activeTaskType].results &&
          contributions[activeTaskType].results[
            selectedContribution[activeTaskType]
          ]
            ? {
                label:
                  contributions[activeTaskType].results[
                    selectedContribution[activeTaskType]
                  ].submitted_prompt ||
                  contributions[activeTaskType].results[
                    selectedContribution[activeTaskType]
                  ].original_prompt,
                value: selectedContribution[activeTaskType],
              }
            : null
        }
        options={
          contributions[activeTaskType] && contributions[activeTaskType].results
            ? contributions[activeTaskType].results.map(
                (contribution, cIndex) => ({
                  label: contribution.submitted_prompt
                    ? contribution.submitted_prompt.substring(0, 100)
                    : contribution.original_prompt
                    ? contribution.original_prompt.substring(0, 100)
                    : "",
                  value: cIndex,
                })
              )
            : []
        }
        onChange={(selectedOption) => {
          setSelectedContribution((prev) => ({
            ...prev,
            [activeTaskType]: selectedOption.value,
          }));
        }}
        styles={{
          control: (provided) => ({
            ...provided,
            borderRadius: "999px",
            background: "#f0f9ff",
            border: "none",
            padding: "0.25rem",
          }),
        }}
      />
      <Box mt={2}>
        <Select
          classNamePrefix="select"
          isSearchable={true}
          isClearable={false}
          placeholder="Select page"
          onChange={(selectedOption) => handlePageChange(selectedOption.value)}
          options={pageOptions}
          value={pageOptions.find(
            (option) => option.value === currentPages[activeTaskType]
          )}
          styles={{
            control: (provided) => ({
              ...provided,
              borderRadius: "999px",
              background: "#f0f9ff",
              border: "none",
              padding: "0.25rem",
            }),
          }}
        />
      </Box>
    </Box>
  );
};

export default ContributionPaginatorSmall;
