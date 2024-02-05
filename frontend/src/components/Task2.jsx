import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Flex,
  HStack,
  Spacer,
  Spinner,
  Text,
  Textarea,
  useBreakpointValue,
  useToast,
} from "@chakra-ui/react";
import Select from "react-select";

import { trackButtonClickGA } from "../helpers/ga.jsx";
import { submitTaskContribution } from "../helpers/task.jsx";
import { getUser, getUserLanguages } from "../helpers/user.jsx";

const Task2 = () => {
  const toast = useToast();

  const [userId, setUserId] = useState(null);

  const [isLoading, setIsLoading] = useState(false);

  const [prompt, setPrompt] = useState("");
  const [completion, setCompletion] = useState("");

  const [languages, setLanguages] = useState([]);
  const [languageOptionsListed, setLanguageOptionsListed] = useState([]);
  const [selectedLanguage, setSelectedLanguage] = useState(null);

  // Responsive sizes for the Textarea elements
  const textareaSize = useBreakpointValue({ base: "300px", md: "200px" });
  const fontSizeSubTitle = useBreakpointValue({ base: "0.75rem", md: "1rem" });

  const [startOfSession, setStartOfSession] = useState(true);

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

    // When the user has only 1 language
    if (languages.length === 1) {
      setSelectedLanguage(languages[0]);
    }
    // When its the start of a session and the user has multiple languages
    else if (startOfSession && languages.length > 1) {
      setSelectedLanguage(null);
    }
  }, [languages]);

  const handleLanguageChange = (value) => {
    setStartOfSession(false);
    setSelectedLanguage(value);
  };

  const handlePromptChange = (e) => {
    setPrompt(e.target.value);
  };

  const handleCompletionChange = (e) => {
    setCompletion(e.target.value);
  };

  const handleSubmit = async () => {
    try {
      setIsLoading(true);
      if (!prompt.trim() || !completion.trim()) {
        toast({
          title: "Not so fast! You forgot something.",
          description:
            "You must write the prompt and completion before submitting.",
          status: "error",
          duration: 3000,
          isClosable: true,
        });
        return;
      } else if (selectedLanguage === null) {
        toast({
          title: "Not so fast! You forgot something.",
          description: "You must select a language before submitting.",
          status: "error",
          duration: 3000,
          isClosable: true,
        });
        return;
      }

      const taskData = {
        submitted_by: userId,
        submitted_prompt: prompt,
        submitted_completion: completion,
        language_id: selectedLanguage.id,
      };

      await submitTaskContribution(taskData);

      setPrompt("");
      setCompletion("");

      toast({
        title: "Task Submitted",
        description: "Task done. Points Updated. Respect Increased.",
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

  // Render the Task 2 UI
  return (
    <>
      <Box>
        <Text fontSize={fontSizeSubTitle} fontWeight="200" as="b" mb={4}>
          Help us add more examples by writing your own prompt and their
          completion in your language.
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
          <HStack>
            <span />
            <Spacer />
            {languageOptionsListed.length > 0 && (
              <Select
                classNamePrefix="select"
                isSearchable={true}
                isClearable={false}
                name="Language"
                defaultValue={
                  languages.length === 1
                    ? languageOptionsListed[0]
                    : { value: null, label: "" }
                }
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
          </HStack>
        </Box>
        <Box mt={4} minW="100%">
          <Box display="flex" justifyContent="space-between">
            <Text fontSize="1.4rem" as="b">
              Prompt
            </Text>
          </Box>
          <Box mt={4}></Box>
          <Textarea
            value={prompt}
            placeholder="Write your prompt here..."
            rounded="2xl"
            backgroundColor="#FFFFFF"
            sx={{ color: "black" }}
            variant="outline"
            height={textareaSize}
            onChange={handlePromptChange}
            dir={selectedLanguage ? selectedLanguage.direction : "ltr"}
          />
        </Box>
        <Box my={4} minW="100%">
          <Box display="flex" justifyContent="space-between">
            <Text fontSize="1.4rem" as="b">
              Completion
            </Text>
          </Box>
          <Box mt={4}></Box>
          <Textarea
            value={completion}
            placeholder="Write your completion here..."
            rounded="2xl"
            backgroundColor="#FFFFFF"
            sx={{ color: "black" }}
            variant="outline"
            height={textareaSize}
            onChange={handleCompletionChange}
            dir={selectedLanguage ? selectedLanguage.direction : "ltr"}
          />
        </Box>
        <Flex
          justifyContent="center"
          alignItems="center"
          className="base:mx-auto mt-2 md:ml-auto"
        >
          <Button
            colorScheme="blue"
            id="submitButton"
            onClick={() => {
              trackButtonClickGA("skip-task2-button");
              handleSubmit();
            }}
            borderRadius={999}
          >
            Submit Entry
          </Button>
        </Flex>
      </Flex>
    </>
  );
};

export default Task2;
