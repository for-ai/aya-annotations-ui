import React from "react";
import { Box, Text, Textarea, useBreakpointValue } from "@chakra-ui/react";

import ThumbsUpDownDisplay from "./ThumbsUpDownDisplay.jsx";

const TaskDetails = ({
  contributions,
  selectedContribution,
  activeTaskType,
}) => {
  const textareaSize = useBreakpointValue({ base: "300px", md: "200px" });
  const feedbackTextareaSize = useBreakpointValue({ base: "75px", md: "50px" });

  return (
    <Box bg="white" rounded="2xl" p="4" boxShadow="md" width="100%">
      {contributions &&
        contributions[activeTaskType] &&
        contributions[activeTaskType].results.length > 0 &&
        activeTaskType === "task1" &&
        contributions[activeTaskType].results && (
          <>
            <Text mt="4" mb="2" fontWeight="bold" text-align="center">
              Prompt
            </Text>
            <Textarea
              mt={4}
              isReadOnly={true}
              rounded="2xl"
              backgroundColor="#FAFAFA"
              variant="outline"
              width="100%"
              height={textareaSize}
              value={
                contributions[activeTaskType].results[
                  selectedContribution[activeTaskType]
                ].submitted_prompt
              }
            />
            <Text mt="6" mb="2" fontWeight="bold">
              Prompt Rating:
              <ThumbsUpDownDisplay
                value={
                  contributions[activeTaskType].results[
                    selectedContribution[activeTaskType]
                  ].prompt_rating
                }
              />
            </Text>
            <Text mt="6" mb="2" fontWeight="bold" text-align="center">
              Completion
            </Text>
            <Textarea
              mt={4}
              isReadOnly={true}
              rounded="2xl"
              backgroundColor="#FAFAFA"
              variant="outline"
              width="100%"
              height={textareaSize}
              value={
                contributions[activeTaskType].results[
                  selectedContribution[activeTaskType]
                ].submitted_completion
              }
            />
            <Text mt="6" mb="2" fontWeight="bold">
              Completion Rating:
              <ThumbsUpDownDisplay
                value={
                  contributions[activeTaskType].results[
                    selectedContribution[activeTaskType]
                  ].completion_rating
                }
              />
            </Text>
          </>
        )}
      {contributions &&
        contributions[activeTaskType] &&
        contributions[activeTaskType].results.length > 0 &&
        activeTaskType === "task2" &&
        contributions[activeTaskType].results && (
          <>
            <Text mt="4" mb="2" fontWeight="bold" text-align="center">
              Prompt
            </Text>
            <Textarea
              mt={4}
              isReadOnly={true}
              rounded="2xl"
              backgroundColor="#FAFAFA"
              variant="outline"
              width="100%"
              height={textareaSize}
              value={
                contributions[activeTaskType].results[
                  selectedContribution[activeTaskType]
                ].submitted_prompt
              }
              mb="4"
            />

            <Text mt="6" mb="2" fontWeight="bold">
              Completion
            </Text>
            <Textarea
              mt={4}
              isReadOnly={true}
              rounded="2xl"
              backgroundColor="#FAFAFA"
              variant="outline"
              width="100%"
              height={textareaSize}
              value={
                contributions[activeTaskType].results[
                  selectedContribution[activeTaskType]
                ].submitted_completion
              }
              mb="4"
            />
          </>
        )}
      {contributions &&
        contributions[activeTaskType] &&
        contributions[activeTaskType].results.length > 0 &&
        activeTaskType === "task3" &&
        contributions[activeTaskType].results && (
          <>
            <Text mt="4" mb="2" fontWeight="bold" text-align="center">
              Original Prompt
            </Text>
            <Textarea
              mt={4}
              isReadOnly={true}
              rounded="2xl"
              backgroundColor="#FAFAFA"
              variant="outline"
              width="100%"
              height={textareaSize}
              value={
                contributions[activeTaskType].results[
                  selectedContribution[activeTaskType]
                ].original_prompt
              }
            />
            <Text mt="6" mb="2" fontWeight="bold" text-align="center">
              Edited Prompt
            </Text>
            <Textarea
              mt={4}
              isReadOnly={true}
              rounded="2xl"
              backgroundColor="#FAFAFA"
              variant="outline"
              width="100%"
              height={textareaSize}
              value={
                contributions[activeTaskType].results[
                  selectedContribution[activeTaskType]
                ].edited_prompt
              }
            />
            <Text mt="6" mb="2" fontWeight="bold">
              Edited Prompt Rating:
              {
                contributions[activeTaskType].results[
                  selectedContribution[activeTaskType]
                ].edited_prompt_rating
              }
            </Text>
            {contributions[activeTaskType].results[
              selectedContribution[activeTaskType]
            ].improved_prompt && (
              <>
                <Text mt="6" mb="2" text-align="center" fontWeight="bold">
                  Improved Edited Prompt
                </Text>
                <Textarea
                  mt={4}
                  isReadOnly={true}
                  rounded="2xl"
                  backgroundColor="white"
                  variant="outline"
                  width="100%"
                  height={textareaSize}
                  value={
                    contributions[activeTaskType].results[
                      selectedContribution[activeTaskType]
                    ].improved_prompt
                  }
                  mb="4"
                />
              </>
            )}

            <Text mt="6" mb="2" fontWeight="bold" text-align="center">
              Original Completion
            </Text>
            <Textarea
              mt={4}
              isReadOnly={true}
              rounded="2xl"
              backgroundColor="#FAFAFA"
              variant="outline"
              width="100%"
              height={textareaSize}
              value={
                contributions[activeTaskType].results[
                  selectedContribution[activeTaskType]
                ].original_completion
              }
            />
            <Text mt="6" mb="2" fontWeight="bold" text-align="center">
              Edited Completion
            </Text>
            <Textarea
              mt={4}
              isReadOnly={true}
              rounded="2xl"
              backgroundColor="#FAFAFA"
              variant="outline"
              width="100%"
              height={textareaSize}
              value={
                contributions[activeTaskType].results[
                  selectedContribution[activeTaskType]
                ].edited_completion
              }
            />
            <Text mt="6" mb="2" fontWeight="bold">
              Edited Completion Rating:
              {
                contributions[activeTaskType].results[
                  selectedContribution[activeTaskType]
                ].edited_completion_rating
              }
            </Text>
            {contributions[activeTaskType].results[
              selectedContribution[activeTaskType]
            ].improved_completion && (
              <>
                <Text mt="6" mb="2" text-align="center" fontWeight="bold">
                  Improved Edited Completion
                </Text>
                <Textarea
                  mt={4}
                  isReadOnly={true}
                  rounded="2xl"
                  backgroundColor="white"
                  variant="outline"
                  width="100%"
                  height={textareaSize}
                  value={
                    contributions[activeTaskType].results[
                      selectedContribution[activeTaskType]
                    ].improved_completion
                  }
                  mb="4"
                />
              </>
            )}
            {contributions[activeTaskType].results[
              selectedContribution[activeTaskType]
            ].improvement_feedback && (
              <>
                <Text mt="6" mb="2" fontWeight="bold" text-align="center">
                  Additional Feedback
                </Text>
                <Textarea
                  mt={4}
                  isReadOnly={true}
                  rounded="2xl"
                  backgroundColor="#FAFAFA"
                  variant="outline"
                  width="100%"
                  height={feedbackTextareaSize}
                  value={
                    contributions[activeTaskType].results[
                      selectedContribution[activeTaskType]
                    ].improvement_feedback
                  }
                />
              </>
            )}
          </>
        )}
    </Box>
  );
};

export default TaskDetails;
