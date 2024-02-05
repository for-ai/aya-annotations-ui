import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Checkbox,
  Flex,
  HStack,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
  Spacer,
  Spinner,
  Stack,
  Switch,
  Text,
  Textarea,
  useBreakpointValue,
  useDisclosure,
  useToast,
} from "@chakra-ui/react";
import { BsFillCheckCircleFill } from "react-icons/bs";
import Select from "react-select";

import { trackButtonClickGA } from "../helpers/ga.jsx";
import {
  getTasks,
  submitTaskAudit,
  submitTaskContributionAudit,
} from "../helpers/task.jsx";
import { getUser, getUserLanguages } from "../helpers/user.jsx";
import ThumbsUpDown from "./ThumbsUpDown.jsx";

const Task1 = () => {
  const toast = useToast();

  const [userId, setUserId] = useState(null);

  const [isEditable, setIsEditable] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const [taskId, setID] = useState("");
  const [prompt, setPrompt] = useState("");
  const [completion, setCompletion] = useState("");
  const [taskIsContributed, setTaskIsContributed] = useState(false);

  const [promptEdited, setPromptEdited] = useState(false);
  const [completionEdited, setCompletionEdited] = useState(false);

  const [languages, setLanguages] = useState([]);
  const [languageOptionsListed, setLanguageOptionsListed] = useState([]);
  const [selectedLanguage, setSelectedLanguage] = useState(null);

  const [isPromptThumbsUp, setIsPromptThumbsUp] = useState(null);
  const [isCompletionThumbsUp, setIsCompletionThumbsUp] = useState(null);

  // Responsive font sizes for Text elements
  const fontSizeBase = useBreakpointValue({ base: "1rem", md: "1.5rem" });
  const fontSizeTitle = useBreakpointValue({ base: "1.5rem", md: "3rem" });
  const fontSizeSubTitle = useBreakpointValue({ base: "0.75rem", md: "1rem" });

  // Responsive sizes for the Textarea elements
  const textareaSize = useBreakpointValue({ base: "300px", md: "200px" });

  const [tasksArray, setTasksArray] = useState([]);
  const [currentTaskIndex, setCurrentTaskIndex] = useState(0);
  const { isOpen, onOpen, onClose } = useDisclosure();

  const [initialPrompt, setInitialPrompt] = useState("");
  const [initialCompletion, setInitialCompletion] = useState("");
  const [promptEditDistance, setPromptEditDistance] = useState(0);
  const [completionEditDistance, setCompletionEditDistance] = useState(0);

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
    if (isPromptThumbsUp !== null && isCompletionThumbsUp !== null) {
      setIsEditable(true);
    }
  }, [isPromptThumbsUp, isCompletionThumbsUp]);

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
      setIsPromptThumbsUp(null);
      setIsCompletionThumbsUp(null);
      setIsEditable(false);
      await updateTasks();
    };

    if (userId && selectedLanguage) {
      resetAndUpdate();
    }
  }, [userId, selectedLanguage]);

  const toggleDisable = () => {
    setIsEditable((prevState) => !prevState);
  };

  const handleLanguageChange = (value) => {
    setCurrentTaskIndex(0);
    setTasksArray([]);
    setSelectedLanguage(value);
  };

  const levenshteinDistance = (str1 = "", str2 = "") => {
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
  };

  const handlePromptChange = (e) => {
    setPromptEditDistance(levenshteinDistance(e.target.value, initialPrompt));
    setPrompt(e.target.value);
    setPromptEdited(true);
  };

  const handleCompletionChange = (e) => {
    setCompletionEditDistance(
      levenshteinDistance(e.target.value, initialCompletion)
    );
    setCompletion(e.target.value);
    setCompletionEdited(true);
  };

  const updateTasks = async () => {
    try {
      setIsLoading(true);

      if (currentTaskIndex < tasksArray.length) {
        const task = tasksArray[currentTaskIndex];
        setID(task["id"]);
        setPrompt(task["prompt"]);
        setCompletion(task["completion"]);
        setInitialPrompt(task["prompt"]);
        setInitialCompletion(task["completion"]);
        setTaskIsContributed(task["is_contributed"]);
        setPromptEditDistance(0);
        setCompletionEditDistance(0);
        setCurrentTaskIndex((prevIndex) => prevIndex + 1);
      } else {
        const tasks = await getTasks(userId, selectedLanguage.id);

        if (tasks && tasks.length > 0) {
          setID(tasks[0]["id"]);
          setPrompt(tasks[0]["prompt"]);
          setCompletion(tasks[0]["completion"]);
          setPromptEditDistance(0);
          setCompletionEditDistance(0);
          setInitialPrompt(tasks[0]["prompt"]);
          setInitialCompletion(tasks[0]["completion"]);
          setTaskIsContributed(tasks[0]["is_contributed"]);
          setTasksArray(tasks);
          // Resetting the index to 1 as we are already showing the first task
          setCurrentTaskIndex(1);
        } else {
          setID(null);
          setPrompt("");
          setCompletion("");
          setInitialPrompt("");
          setInitialCompletion("");
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

  const handleSubmit = async () => {
    try {
      setIsLoading(true);

      if (isPromptThumbsUp === null || isCompletionThumbsUp === null) {
        toast({
          title: "Not so fast! You forgot something.",
          description: "You must rate the task before submitting.",
          status: "error",
          duration: 3000,
          isClosable: true,
        });
        return;
      }

      if (
        promptEdited === false &&
        completionEdited === false &&
        isOpen === false
      ) {
        onOpen();
        return;
      }

      if (isOpen === true) {
        onClose();
      }

      if (taskIsContributed === true) {
        const taskData = {
          task_contribution_id: taskId,
          submitted_by: userId,
          submitted_prompt: prompt,
          submitted_completion: completion,
          prompt_edited: promptEdited,
          completion_edited: completionEdited,
          prompt_rating: isPromptThumbsUp,
          completion_rating: isCompletionThumbsUp,
        };

        await submitTaskContributionAudit(taskData);
      } else {
        const taskData = {
          task_id: taskId,
          submitted_by: userId,
          submitted_prompt: prompt,
          submitted_completion: completion,
          prompt_edited: promptEdited,
          completion_edited: completionEdited,
          prompt_rating: isPromptThumbsUp,
          completion_rating: isCompletionThumbsUp,
        };

        await submitTaskAudit(taskData);
      }

      setIsEditable(false);
      setPromptEdited(false);
      setCompletionEdited(false);
      setIsPromptThumbsUp(null);
      setIsCompletionThumbsUp(null);
      setInitialPrompt("");
      setInitialCompletion("");
      setPromptEditDistance(0);
      setCompletionEditDistance(0);

      trackButtonClickGA("submit-task1-button");

      await updateTasks();

      toast({
        title: "Task Submitted",
        description: "Task done. Points Updated. Respect Increased.",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      console.error(error);
      toast({
        title: "Something went wrong!",
        description: `Please try again or message in the Aya Discord
        for help in the #feedback-ui channel.`,
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleSkip = async () => {
    try {
      setIsEditable(false);
      setPromptEdited(false);
      setCompletionEdited(false);
      setIsPromptThumbsUp(null);
      setIsCompletionThumbsUp(null);
      setInitialPrompt("");
      setInitialCompletion("");

      trackButtonClickGA("skip-task1-button");

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

  // Render the Task 1 UI
  return (
    <>
      <Modal
        isCentered
        size={"xl"}
        closeOnOverlayClick={false}
        isOpen={isOpen}
        onClose={onClose}
      >
        <ModalOverlay bg="blackAlpha.300" backdropFilter="blur(10px)" />
        <ModalContent>
          <ModalHeader>Wait a Second! Let's recap...</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <Text color={"yellow.800"}>
              <b>Gentle Reminder:</b> You are going to submit feedback without
              editing the prompt and completion. Doing so would mean you'll get
              only 1 point for rating the task.
            </Text>
            <Text color={"green"}>
              <b>Good News</b> is you can get 2 more points by editing the
              prompts and completion🥳. If you are not sure what to edit, here
              are some things you can make sure are correct:
            </Text>
            <Stack mt={1} spacing={4}>
              <Checkbox>
                Grammar and spellings of Prompt and Completion is correct.
              </Checkbox>
              <Checkbox>
                Instruction on what to do is present and is very clear.
              </Checkbox>
              <Checkbox>
                The Completion does the task perfectly and is very clear to
                understand.
              </Checkbox>
            </Stack>
          </ModalBody>

          <ModalFooter>
            <Button colorScheme="blue" mr={3} onClick={handleSubmit}>
              Continue
            </Button>
            <Button onClick={onClose}>Go Back</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
      <Box>
        <Text fontSize={fontSizeSubTitle} fontWeight="200" as="b" mb={4}>
          Help improve the model performance by rating the prompt-completion
          pairs below
        </Text>
      </Box>
      <Flex direction="column" align="center" justify="center" mx="auto" py={3}>
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
        <Box minW="100%">
          <HStack mb={4}>
            <Switch
              colorScheme="teal"
              size="lg"
              onChange={toggleDisable}
              isChecked={isEditable}
              isDisabled={
                isPromptThumbsUp === null || isCompletionThumbsUp === null
              }
            />
            <Text
              fontSize={{ base: "sm", md: "md" }}
              py={1}
              px={3}
              color={isEditable ? "teal.100" : "blue.100"}
              backgroundColor={isEditable ? "teal.500" : "blue.500"}
              borderRadius="9999px"
            >
              {isEditable ? "Edit" : "Read"} Mode
            </Text>
            <Spacer />
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
                    width: 150,
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
          </HStack>
          <Box display="flex" justifyContent="space-between">
            <Text fontSize="1.4rem" as="b">
              Prompt
            </Text>
            <Box>
              {isPromptThumbsUp === null && (
                <ThumbsUpDown
                  isThumbsUp={isPromptThumbsUp}
                  setIsThumbsUp={setIsPromptThumbsUp}
                />
              )}
            </Box>
          </Box>
          <Flex
            direction={{ base: "column", md: "row" }}
            alignItems={{ base: "left", md: "center" }}
          >
            <Text>Look out for: </Text>
            <Flex direction="row" alignItems="center">
              <BsFillCheckCircleFill
                color="green"
                className="base:ml-2 base:mr-1 mx-1"
              />
              <Text> Correct Grammar </Text>
            </Flex>
            <Flex direction="row" alignItems="center">
              <BsFillCheckCircleFill color="green" className="mx-1" />
              <Text> Reasonable Length </Text>
            </Flex>
            <Flex direction="row" alignItems="center">
              <BsFillCheckCircleFill color="green" className="mx-1" />
              <Text> Clear Instructions </Text>
            </Flex>
          </Flex>
          <Textarea
            mt={4}
            isDisabled={!isEditable}
            value={prompt}
            rounded="2xl"
            backgroundColor={isEditable ? "#FFFFFF" : "#FAFAFA"}
            variant="outline"
            height={textareaSize}
            onChange={handlePromptChange}
            dir={selectedLanguage ? selectedLanguage.direction : "ltr"}
            _disabled={{ opacity: "1", color: "rgba(0, 0, 0, 0.6)" }}
          />
        </Box>
        <Text
          mt={2}
          px={2}
          py={1}
          color="green.700"
          bgColor="green.200"
          borderRadius="lg"
          alignSelf={"self-start"}
          fontWeight="bold"
        >
          Edit Distance[Prompt]: {promptEditDistance}
        </Text>
        <Box minW="100%" mt={4} mb={4}>
          <Box display="flex" justifyContent="space-between">
            <Text fontSize="1.4rem" as="b">
              Completion
            </Text>
            <Box>
              {isCompletionThumbsUp === null && (
                <ThumbsUpDown
                  isThumbsUp={isCompletionThumbsUp}
                  setIsThumbsUp={setIsCompletionThumbsUp}
                />
              )}
            </Box>
          </Box>
          <Flex
            direction={{ base: "column", md: "row" }}
            alignItems={{ base: "left", md: "center" }}
          >
            <Text>Look out for: </Text>
            <Flex direction="row" alignItems="center">
              <BsFillCheckCircleFill
                color="green"
                className="base:ml-2 base:mr-1 mx-1"
              />
              <Text> Clear Answer </Text>
            </Flex>
            <Flex direction="row" alignItems="center">
              <BsFillCheckCircleFill color="green" className="mx-1" />
              <Text> Full Sentences with Correct Answer </Text>
            </Flex>
            <Flex direction="row" alignItems="center">
              <BsFillCheckCircleFill color="green" className="mx-1" />
              <Text> Reasonable Length </Text>
            </Flex>
          </Flex>
          <Box mt={4}></Box>
          <Textarea
            isDisabled={!isEditable}
            value={completion}
            rounded="2xl"
            backgroundColor={isEditable ? "#FFFFFF" : "#FAFAFA"}
            variant="outline"
            height={textareaSize}
            onChange={handleCompletionChange}
            dir={selectedLanguage ? selectedLanguage.direction : "ltr"}
            _disabled={{ opacity: "1", color: "rgba(0, 0, 0, 0.6)" }}
          />
        </Box>
        <Text
          mt={2}
          px={2}
          py={1}
          color="green.700"
          bgColor="green.200"
          borderRadius="lg"
          alignSelf={"self-start"}
          fontWeight="bold"
        >
          Edit Distance[Completion]: {completionEditDistance}
        </Text>
        <Flex
          justifyContent="center"
          alignItems="center"
          className="base:mx-auto mt-2 md:ml-auto"
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
            onClick={() => {
              handleSubmit();
            }}
            marginLeft="1rem"
            borderRadius={999}
          >
            Submit {isEditable ? "Entry" : "Feedback"}
          </Button>
        </Flex>
        {taskId && (
          <>
            <Flex justifyContent="center" alignItems="center">
              <Text pt="2rem" fontSize="xs" style={{ opacity: 0.3 }}>
                Task ID: {taskId}
              </Text>
            </Flex>
          </>
        )}
      </Flex>
    </>
  );
};

export default Task1;
