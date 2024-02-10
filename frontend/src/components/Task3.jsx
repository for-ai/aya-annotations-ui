import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Collapse,
  Fade,
  Flex,
  Heading,
  Image,
  Radio,
  RadioGroup,
  SimpleGrid,
  Spacer,
  Spinner,
  Switch,
  Text,
  Textarea,
  VStack,
  useBreakpointValue,
  useToast,
} from "@chakra-ui/react";
import { diff_match_patch } from "diff-match-patch";
import Select from "react-select";

import {
  getUserFeedbackTasks,
  submitTaskAuditContributionReview,
  submitTaskAuditReview,
} from "../helpers/task.jsx";
import { getUser, getUserLanguages } from "../helpers/user.jsx";

const computeDifference = (oldText, newText) => {
  const dmp = new diff_match_patch();
  const diffs = dmp.diff_main(oldText, newText);
  dmp.diff_cleanupSemantic(diffs);

  return diffs.map(([type, text]) => {
    switch (type) {
      case -1:
        return (
          <span style={{ color: "red", textDecoration: "line-through" }}>
            {text}
          </span>
        );
      case 1:
        return <span style={{ color: "green" }}>{text}</span>;
      default:
        return text;
    }
  });
};

const Task3 = () => {
  const toast = useToast();

  const [userId, setUserId] = useState(null);
  const [contributedBy, setContributedBy] = useState(null);
  const [contributedByImage, setContributedByImage] = useState(null);

  const [isLoading, setIsLoading] = useState(false);

  const [taskAuditId, setTaskAuditId] = useState("");
  const [taskIsContributed, setTaskIsContributed] = useState(false);

  const [languages, setLanguages] = useState([]);
  const [languageOptionsListed, setLanguageOptionsListed] = useState([]);
  const [selectedLanguage, setSelectedLanguage] = useState(null);

  const [originalPrompt, setOriginalPrompt] = useState("");
  const [originalCompletion, setOriginalCompletion] = useState("");
  const [editedPrompt, setEditedPrompt] = useState("");
  const [editedCompletion, setEditedCompletion] = useState("");

  // For improved prompt and completion textareas when score < 5
  const [improvedEditedPrompt, setImprovedEditedPrompt] = useState("");
  const [improvedEditedCompletion, setImprovedEditedCompletion] = useState("");

  // For radio buttons
  const [editedPromptRating, setEditedPromptRating] = useState("");
  const [editedCompletionRating, setEditedCompletionRating] = useState("");

  //For Edit View
  const [showDiffPrompt, setShowDiffPrompt] = useState(false);
  const [showDiffCompletion, setShowDiffCompletion] = useState(false);

  // For additional feedback textarea
  const [feedback, setFeedback] = useState("");

  // Responsive font size for Text elements
  const fontSizeSubTitle = useBreakpointValue({ base: "0.75rem", md: "1rem" });

  // Responsive size for the Textarea elements
  const textareaSize = useBreakpointValue({ base: "300px", md: "200px" });
  const feedbackTextareaSize = useBreakpointValue({ base: "75px", md: "50px" });

  const [showImprovedEditedPrompt, setShowImprovedEditedPrompt] =
    useState(false);
  const [showImprovedEditedCompletion, setShowImprovedEditedCompletion] =
    useState(false);
  const [promptEditDistance, setPromptEditDistance] = useState(0);
  const [completionEditDistance, setCompletionEditDistance] = useState(0);

  const [tasksArray, setTasksArray] = useState([]);
  const [currentTaskIndex, setCurrentTaskIndex] = useState(0);

  const DiffDisplay = ({ oldText, newText }) => {
    const diffs = computeDifference(oldText, newText);
    return (
      <Box
        mt={4}
        rounded="2xl"
        backgroundColor="#FAFAFA"
        variant="outline"
        width="100%"
        height={textareaSize}
        border="1px solid #E3E3E3"
        dir={selectedLanguage ? selectedLanguage.direction : "ltr"}
        p={2}
        style={{ whiteSpace: "pre-wrap", overflowY: "auto" }} // to preserve line breaks, spaces and apply scrollable if the text goes too long
      >
        {diffs}
      </Box>
    );
  };

  useEffect(() => {
    const user = getUser();
    if (user && user.id) {
      setUserId(user.id);

      // Fetch the user's language list
      (async () => {
        const fetchedLanguages = await getUserLanguages();
        setLanguages(fetchedLanguages);
      })();
    }
  }, []);

  useEffect(() => {
    setLanguageOptionsListed(
      languages.map((option) => ({
        value: option,
        label: option.name,
      }))
    );

    // Set the selected language to the first language in the list
    const value = languages.length > 0 ? languages[0] : null;
    setSelectedLanguage(value);
  }, [languages]);

  useEffect(() => {
    const resetAndUpdate = async () => {
      setCurrentTaskIndex(0);
      setTasksArray([]);
      await updateTasks();
    };

    if (userId && selectedLanguage) {
      resetAndUpdate();
    }
  }, [userId, selectedLanguage]);

  useEffect(() => {
    if (editedPromptRating && editedPromptRating < 5) {
      if (improvedEditedPrompt === "") {
        setImprovedEditedPrompt(editedPrompt);
      }
      setShowImprovedEditedPrompt(true);
    } else {
      setShowImprovedEditedPrompt(false);
    }
  }, [editedPromptRating]);

  useEffect(() => {
    if (editedCompletionRating && editedCompletionRating < 5) {
      if (improvedEditedCompletion === "") {
        setImprovedEditedCompletion(editedCompletion);
      }
      setShowImprovedEditedCompletion(true);
    } else {
      setShowImprovedEditedCompletion(false);
    }
  }, [editedCompletionRating]);

  const levenshteinDistance = (str1 = "", str2 = "") => {
    if (str1.length <= 30000 && str2.length <= 30000) {
      const track = Array(str2.length + 1)
        .fill(null)
        .map(() => Array(str1.length + 1).fill(null));

      for (let i = 0; i <= str1.length; i += 1) {
        track[0][i] = i;
      }

      for (let j = 1; j <= str2.length; j += 1) {
        track[j][0] = j;
      }

      for (let j = 1; j <= str2.length; j += 1) {
        for (let i = 1; i <= str1.length; i += 1) {
          const substitutionCost = str1[i - 1] === str2[j - 1] ? 0 : 1;

          track[j][i] = Math.min(
            track[j - 1][i] + 1, // deletion
            track[j][i - 1] + 1, // insertion
            track[j - 1][i - 1] + substitutionCost // substitution
          );
        }
      }

      return track[str2.length][str1.length];
    } else {
      return "Too long to compute";
    }
  };

  const updateTasks = async () => {
    try {
      setIsLoading(true);
      // Get tasks for reviewers
      if (currentTaskIndex < tasksArray.length) {
        const task = tasksArray[currentTaskIndex];
        setTaskAuditId(task["id"]);
        setTaskIsContributed(task["is_contributed"]);
        setContributedBy(task["contributed_by"]);
        setContributedByImage(task["contributed_by_image"]);
        setOriginalPrompt(task["original_prompt"]);
        setOriginalCompletion(task["original_completion"]);
        setEditedPrompt(task["edited_prompt"]);
        setEditedCompletion(task["edited_completion"]);
        setPromptEditDistance(
          levenshteinDistance(task["original_prompt"], task["edited_prompt"])
        );
        setCompletionEditDistance(
          levenshteinDistance(
            task["original_completion"],
            task["edited_completion"]
          )
        );
        setCurrentTaskIndex((prevIndex) => prevIndex + 1);
      } else {
        const results = await getUserFeedbackTasks(userId, selectedLanguage.id);
        const tasks = results.task_audits;
        if (tasks && tasks.length > 0) {
          setTaskAuditId(tasks[0]["id"]);
          setTaskIsContributed(tasks[0]["is_contributed"]);
          setContributedBy(tasks[0]["contributed_by"]);
          setContributedByImage(tasks[0]["contributed_by_image"]);
          setOriginalPrompt(tasks[0]["original_prompt"]);
          setOriginalCompletion(tasks[0]["original_completion"]);
          setEditedPrompt(tasks[0]["edited_prompt"]);
          setEditedCompletion(tasks[0]["edited_completion"]);
          setPromptEditDistance(
            levenshteinDistance(
              tasks[0]["original_prompt"],
              tasks[0]["edited_prompt"]
            )
          );
          setCompletionEditDistance(
            levenshteinDistance(
              tasks[0]["original_completion"],
              tasks[0]["edited_completion"]
            )
          );
          setTasksArray(tasks);
          // Resetting the index to 1 as we are already showing the first task
          setCurrentTaskIndex(1);
        } else {
          setTaskAuditId(null);
          setTaskIsContributed(false);
          setOriginalPrompt("");
          setOriginalCompletion("");
          setEditedPrompt("");
          setEditedCompletion("");
          setEditedPromptRating("");
          setEditedCompletionRating("");
          setPromptEditDistance(0);
          setCompletionEditDistance(0);

          toast({
            title: "No Tasks Left!",
            description:
              "Thanks a lot for helping out! Come back later for more tasks.",
            status: "warning",
            duration: 3000,
            isClosable: true,
          });
        }
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLanguageChange = (value) => {
    setCurrentTaskIndex(0);
    setTasksArray([]);
    setSelectedLanguage(value);
  };

  const handleFeedbackChange = (e) => {
    setFeedback(e.target.value);
  };

  const handleSubmit = async () => {
    try {
      setIsLoading(true);
      if (editedPromptRating === "" || editedCompletionRating === "") {
        toast({
          title: "Not so fast! You forgot something.",
          description:
            "You must complete the questions marked Required before submitting.",
          status: "error",
          duration: 3000,
          isClosable: true,
        });
        return;
      }

      let taskData;
      if (taskIsContributed) {
        taskData = {
          task_contribution_audit_id: taskAuditId,
          submitted_by: userId,
          edited_prompt_rating: editedPromptRating,
          edited_completion_rating: editedCompletionRating,
          improved_edited_prompt:
            editedPromptRating < 5 && editedPrompt !== improvedEditedPrompt
              ? improvedEditedPrompt
              : null,
          improved_edited_completion:
            editedCompletionRating < 5 &&
            editedCompletion !== improvedEditedCompletion
              ? improvedEditedCompletion
              : null,
          feedback: feedback,
        };
        await submitTaskAuditContributionReview(taskData);
      } else {
        taskData = {
          task_audit_id: taskAuditId,
          submitted_by: userId,
          edited_prompt_rating: editedPromptRating,
          edited_completion_rating: editedCompletionRating,
          improved_edited_prompt:
            editedPromptRating < 5 && editedPrompt !== improvedEditedPrompt
              ? improvedEditedPrompt
              : null,
          improved_edited_completion:
            editedCompletionRating < 5 &&
            editedCompletion !== improvedEditedCompletion
              ? improvedEditedCompletion
              : null,
          feedback: feedback,
        };
        await submitTaskAuditReview(taskData);
      }

      setEditedPromptRating("");
      setEditedCompletionRating("");
      setFeedback("");
      setImprovedEditedPrompt("");
      setImprovedEditedCompletion("");

      await updateTasks();

      toast({
        title: "Feedback Submitted",
        description: "Thank you for your feedback.",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSkip = async () => {
    try {
      setEditedPromptRating("");
      setEditedCompletionRating("");
      setFeedback("");
      setImprovedEditedPrompt("");
      setImprovedEditedCompletion("");

      await updateTasks();

      toast({
        title: "Task Skipped",
        description: "If it's fate you'll come back to this task later.",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <>
      <Box>
        <Text fontSize={fontSizeSubTitle} fontWeight="200" as="b" mb={4}>
          Help rate other users edited prompts and completions.
        </Text>
      </Box>
      <Box
        alignItems="center"
        mb={4}
        justifyContent="center"
        display={{ base: "block", md: "flex" }}
      >
        <Flex direction="column" align="center">
          {isLoading && (
            <Spinner
              thickness="4px"
              speed="0.65s"
              emptyColor="gray.200"
              color="blue.500"
              size="lg"
              m="1.5rem"
            />
          )}
        </Flex>
      </Box>
      <Box minW="100%" mt={4}>
        <Flex justifyContent="space-between" alignItems="center" mb={4}>
          <Flex alignItems="center">
            <Text
              fontSize={fontSizeSubTitle}
              fontWeight="500"
              as="b"
              mr={2}
              display={{ base: "none", md: "block" }}
            >
              Contributed by:
            </Text>
            <Image
              borderRadius="full"
              boxSize={{ base: "2.25rem", md: "2.5rem" }}
              src={contributedByImage}
              mr={2}
            />
            <Text fontSize={fontSizeSubTitle} fontWeight="200" as="b">
              {contributedBy}
            </Text>
          </Flex>
          {languageOptionsListed.length > 0 && (
            <Select
              classNamePrefix="select"
              isSearchable={true}
              isClearable={false}
              name="Language"
              defaultValue={languageOptionsListed[0]}
              options={languageOptionsListed}
              onChange={(selectedOption) => {
                handleLanguageChange(selectedOption.value);
              }}
              styles={{
                control: (provided) => ({
                  ...provided,
                  width: 200,
                  borderRadius: "999px",
                  background: "#f0f9ff",
                  border: "none",
                  padding: "0.25rem",
                  "@media (min-width: 768px)": {
                    width: 250,
                  },
                }),
              }}
            />
          )}
        </Flex>
      </Box>
      <Box w="full" display="flex" justifyContent="center">
        <SimpleGrid
          columns={2}
          spacing={4}
          templateColumns={{ base: "repeat(1, 1fr)", lg: "repeat(2, 1fr)" }}
          width="100%"
        >
          <Box
            p={6}
            border="solid 1px"
            backgroundColor="#f0f9ff"
            borderColor="gray.100"
            rounded="md"
            shadow="sm"
          >
            <Box bg="#f5f5f5" p={2} rounded="md">
              <Heading textAlign="center" size="md">
                Step 1: Prompts
              </Heading>
            </Box>
            <VStack spacing={8} align="stretch" mt={4}>
              <Box my={2}>
                <Text fontSize="1rem" fontWeight="bold">
                  Read the Original Prompt
                </Text>
                <Textarea
                  mt={4}
                  value={originalPrompt}
                  rounded="2xl"
                  backgroundColor="#FAFAFA"
                  variant="outline"
                  width="100%"
                  height={textareaSize}
                  dir={selectedLanguage ? selectedLanguage.direction : "ltr"}
                  _disabled={{ opacity: "1", color: "rgba(0, 0, 0, 0.6)" }}
                />
              </Box>
              <Box my={2}>
                <Flex>
                  <Text fontSize="1rem" fontWeight="bold">
                    Read the Edited Prompt
                  </Text>
                  <Spacer />
                  <Switch
                    colorScheme="teal"
                    size="md"
                    pr={1}
                    onChange={() => setShowDiffPrompt(!showDiffPrompt)}
                    isChecked={showDiffPrompt}
                  />
                  <Text fontSize="0.8rem" fontWeight="bold">
                    Show Edits
                  </Text>
                </Flex>
                {showDiffPrompt ? (
                  <DiffDisplay
                    oldText={originalPrompt}
                    newText={editedPrompt}
                  />
                ) : (
                  <Textarea
                    mt={4}
                    value={editedPrompt}
                    rounded="2xl"
                    backgroundColor="#FAFAFA"
                    variant="outline"
                    width="100%"
                    height={textareaSize}
                    dir={selectedLanguage ? selectedLanguage.direction : "ltr"}
                    _disabled={{ opacity: "1", color: "rgba(0, 0, 0, 0.6)" }}
                  />
                )}
                <Text mt={2} color="green.700">
                  Edit Distance[Prompt]: {promptEditDistance}
                </Text>
              </Box>
              <Box my={2}>
                <Text fontSize="0.8rem" color="red" mt={2}>
                  * Required
                </Text>
                <Text fontSize="1rem" as="b">
                  Is the edited prompt an improvement over the original?
                </Text>
                <RadioGroup
                  value={editedPromptRating}
                  onChange={setEditedPromptRating}
                >
                  <VStack alignItems="flex-start">
                    <Radio value="1">1 - Much worse than Original</Radio>
                    <Radio value="2">2 - Worse than original</Radio>
                    <Radio value="3">
                      3 - No noticeable difference compared to the original
                    </Radio>
                    <Radio value="4">4 - Better than original</Radio>
                    <Radio value="5">5 - Much better than original</Radio>
                  </VStack>
                </RadioGroup>
              </Box>
              {editedPromptRating && editedPromptRating < 5 && (
                <Fade
                  in={showImprovedEditedPrompt}
                  transition={{ duration: 0.7 }}
                >
                  <Collapse in={showImprovedEditedPrompt} animateOpacity>
                    <Box my={2}>
                      <Text fontSize="0.9rem" color="gray" mt={2}>
                        (Optional)
                      </Text>
                      <Box display="flex" justifyContent="space-between">
                        <Text fontSize="1rem" as="b" mb={{ base: 4, md: 0 }}>
                          Further improve the prompt
                        </Text>
                      </Box>
                      <Textarea
                        mt={4}
                        value={improvedEditedPrompt}
                        onChange={(e) =>
                          setImprovedEditedPrompt(e.target.value)
                        }
                        rounded="2xl"
                        backgroundColor="#FAFAFA"
                        variant="outline"
                        dir={
                          selectedLanguage ? selectedLanguage.direction : "ltr"
                        }
                        height={textareaSize}
                      />
                    </Box>
                  </Collapse>
                </Fade>
              )}
            </VStack>
          </Box>
          <Box
            p={6}
            border="solid 1px"
            backgroundColor="#f0f9ff"
            borderColor="gray.100"
            rounded="md"
            shadow="sm"
          >
            <Box bg="#f5f5f5" p={2} rounded="md">
              <Heading textAlign="center" size="md">
                Step 2: Completions
              </Heading>
            </Box>
            <VStack spacing={8} align="stretch" mt={4}>
              <Box my={2}>
                <Text fontSize="1rem" fontWeight="bold">
                  Read the Original Completion
                </Text>
                <Textarea
                  mt={4}
                  value={originalCompletion}
                  rounded="2xl"
                  backgroundColor="#FAFAFA"
                  variant="outline"
                  width="100%"
                  height={textareaSize}
                  dir={selectedLanguage ? selectedLanguage.direction : "ltr"}
                  _disabled={{ opacity: "1", color: "rgba(0, 0, 0, 0.6)" }}
                />
              </Box>
              <Box my={2}>
                <Flex>
                  <Text fontSize="1rem" fontWeight="bold">
                    Read the Edited Completion
                  </Text>
                  <Spacer />
                  <Switch
                    colorScheme="teal"
                    size="md"
                    pr={1}
                    onChange={() => setShowDiffCompletion(!showDiffCompletion)}
                    isChecked={showDiffCompletion}
                  />
                  <Text fontSize="0.8rem" fontWeight="bold">
                    Show Edits
                  </Text>
                </Flex>
                {showDiffCompletion ? (
                  <DiffDisplay
                    oldText={originalCompletion}
                    newText={editedCompletion}
                  />
                ) : (
                  <Textarea
                    mt={4}
                    value={editedCompletion}
                    rounded="2xl"
                    backgroundColor="#FAFAFA"
                    variant="outline"
                    width="100%"
                    height={textareaSize}
                    dir={selectedLanguage ? selectedLanguage.direction : "ltr"}
                    _disabled={{ opacity: "1", color: "rgba(0, 0, 0, 0.6)" }}
                  />
                )}
                <Text mt={2} color="green.700">
                  Edit Distance[Completion]: {completionEditDistance}
                </Text>
              </Box>
              <Box my={2}>
                <Text fontSize="0.8rem" color="red" mt={2}>
                  * Required
                </Text>
                <Text fontSize="1rem" as="b">
                  Is the edited completion an improvement over the original?
                </Text>
                <RadioGroup
                  value={editedCompletionRating}
                  onChange={setEditedCompletionRating}
                >
                  <VStack alignItems="flex-start">
                    <Radio value="1">1 - Much worse than Original</Radio>
                    <Radio value="2">2 - Worse than original</Radio>
                    <Radio value="3">
                      3 - No noticeable difference compared to the original
                    </Radio>
                    <Radio value="4">4 - Better than original</Radio>
                    <Radio value="5">5 - Much better than original</Radio>
                  </VStack>
                </RadioGroup>
              </Box>
              {editedCompletionRating && editedCompletionRating < 5 && (
                <Fade
                  in={showImprovedEditedCompletion}
                  transition={{ duration: 0.7 }}
                >
                  <Collapse in={showImprovedEditedCompletion} animateOpacity>
                    <Box my={2}>
                      <Text fontSize="0.9rem" color="gray" mt={2}>
                        (Optional)
                      </Text>
                      <Box display="flex" justifyContent="space-between">
                        <Text fontSize="1rem" as="b" mb={{ base: 4, md: 0 }}>
                          Further improve the completion
                        </Text>
                      </Box>
                      <Textarea
                        mt={4}
                        value={improvedEditedCompletion}
                        onChange={(e) =>
                          setImprovedEditedCompletion(e.target.value)
                        }
                        rounded="2xl"
                        backgroundColor="#FAFAFA"
                        variant="outline"
                        width="100%"
                        dir={
                          selectedLanguage ? selectedLanguage.direction : "ltr"
                        }
                        height={textareaSize}
                      />
                    </Box>
                  </Collapse>
                </Fade>
              )}
            </VStack>
          </Box>
        </SimpleGrid>
      </Box>
      <Box mt="4rem" mb={2}>
        <Text fontSize="0.9rem" color="gray" mt={2}>
          (Optional)
        </Text>
        <Text fontSize="1rem" as="b" mt={8}>
          Why did you give this rating?
        </Text>
        <Textarea
          value={feedback}
          placeholder="Enter your feedback here..."
          onChange={handleFeedbackChange}
          mt={4}
          rounded="2xl"
          backgroundColor="#FAFAFA"
          variant="outline"
          height={feedbackTextareaSize}
          width="100%"
          dir={selectedLanguage ? selectedLanguage.direction : "ltr"}
          _disabled={{ opacity: "1", color: "rgba(0, 0, 0, 0.6)" }}
        />
      </Box>
      <Flex
        justifyContent="center"
        alignItems="center"
        className="base:mx-auto mt-8 md:ml-auto"
      >
        <Button
          colorScheme="gray"
          id="skipButton"
          onClick={() => {
            handleSkip();
          }}
          borderRadius={999}
          px={{ base: "3rem", md: "4rem" }}
        >
          Skip
        </Button>
        <Button
          colorScheme="blue"
          id="submitButton"
          marginLeft="1rem"
          borderRadius={999}
          onClick={() => {
            handleSubmit();
          }}
        >
          Submit Feedback
        </Button>
      </Flex>
      {taskAuditId && (
        <>
          <Flex justifyContent="center" alignItems="center">
            <Text pt="2rem" fontSize="xs" style={{ opacity: 0.3 }}>
              Task ID: {taskAuditId}
            </Text>
          </Flex>
        </>
      )}
    </>
  );
};

export default Task3;
