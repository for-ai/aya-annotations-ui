import React from "react";
import { Card, CardBody, Text } from "@chakra-ui/react";

const ContributionCard = ({ contribution, selected, onSelect }) => {
  const formatDate = (dateString) => {
    const date = new Date(dateString);

    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0"); // month starts at 0 in JS
    const day = String(date.getDate()).padStart(2, "0");
    const hour = String(date.getHours()).padStart(2, "0");
    const minute = String(date.getMinutes()).padStart(2, "0");
    const second = String(date.getSeconds()).padStart(2, "0");

    return `${year}-${month}-${day} ${hour}-${minute}-${second}`;
  };

  return (
    <Card>
      <CardBody
        onClick={onSelect}
        cursor="pointer"
        borderWidth={selected ? "2px" : "1px"}
        borderColor={selected ? "blue.500" : "gray.200"}
        borderRadius="md"
        transition="all 0.2s"
        _hover={{ borderColor: "blue.500" }}
        p="4"
        boxShadow="md"
      >
        <Text>
          {contribution.submitted_prompt // If type I or II
            ? contribution.submitted_prompt.substring(0, 100)
            : contribution.improved_prompt // If type III
            ? contribution.improved_prompt.substring(0, 100)
            : formatDate(contribution.created_at)}
        </Text>
      </CardBody>
    </Card>
  );
};

export default ContributionCard;
