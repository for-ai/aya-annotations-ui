import React, { useEffect, useState } from "react";
import {
  Button,
  Center,
  Container,
  Text,
  VStack,
  useToast,
} from "@chakra-ui/react";
import axios from "axios";

import { getAgeGroupOptions } from "../helpers/ageGroup.jsx";
import { getApiUrl } from "../helpers/config.jsx";
import { getCountryOptions } from "../helpers/country.jsx";
import {
  trackButtonClickGA,
  trackUserAddDetailsAbandonedGA,
} from "../helpers/ga.jsx";
import { getGenderOptions } from "../helpers/gender.jsx";
import { getLanguageOptions } from "../helpers/language.jsx";
import { updateUserProfile } from "../helpers/user.jsx";
import DialectInput from "./DialectInput";
import MultiSelectDropdown from "./MultiSelectDropdown";
import SingleSelectDropdown from "./SingleSelectDropdown";

function GetDetails() {
  const toast = useToast();

  const [languageList, setLanguageList] = useState([]);
  const [countryList, setCountryList] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState(null);
  const [selectedLanguages, setSelectedLanguages] = useState([]);

  const [genderList, setGenderList] = useState([]);
  const [ageGroupList, setAgeGroupList] = useState([]);
  const [selectedGender, setSelectedGender] = useState(null);
  const [selectedAgeBucket, setSelectedAgeBucket] = useState(null);

  const [dialects, setDialects] = useState([]);

  const [currentUserSettings, setCurrentUserSettings] = useState({});

  const [loading, setLoading] = useState(true);

  const handleBeforeUnload = (event) => {
    trackUserAddDetailsAbandonedGA();
  };

  useEffect(() => {
    window.addEventListener("beforeunload", handleBeforeUnload);

    return () => {
      window.removeEventListener("beforeunload", handleBeforeUnload);
    };
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);

        const [languages, countries] = await Promise.all([
          getLanguageOptions(),
          getCountryOptions(),
        ]);
        setLanguageList(languages);
        setCountryList(countries);

        const genders = getGenderOptions();
        setGenderList(genders);

        const ageGroup = getAgeGroupOptions();
        setAgeGroupList(ageGroup);

        const apiUrl = await getApiUrl();
        const user_id = JSON.parse(localStorage.getItem("user"))["id"];
        const response = await axios.get(`${apiUrl}/users/${user_id}`);
        const user = response.data;
        setCurrentUserSettings(user);

        const currentCountryCode = user.country_code;
        if (currentCountryCode) {
          const currentCountryOption = countries.find(
            (option) => option.id === currentCountryCode
          );
          setSelectedCountry(currentCountryOption);
        }

        const currentLanguageCodes = user.language_codes;
        if (currentLanguageCodes && currentLanguageCodes.length !== 0) {
          const currentLanguagesOption = languages.filter(
            (option) =>
              currentLanguageCodes && currentLanguageCodes.includes(option.id)
          );
          setSelectedLanguages(currentLanguagesOption);
        }

        const currentGender = user.gender;
        if (currentGender) {
          const currentGenderOption = genders.find(
            (option) => option.id === currentGender
          );
          setSelectedGender(currentGenderOption);
        }

        const currentAgeGroup = user.age_range;
        if (currentAgeGroup) {
          const ageRangeCode = `${currentAgeGroup[0]}-${currentAgeGroup[1]}`;
          const currentAgeGroupOption = ageGroup.find(
            (option) => option.code === ageRangeCode
          );
          setSelectedAgeBucket(currentAgeGroupOption);
        }

        const currentDialects = user.dialects;
        setDialects(Array.isArray(currentDialects) ? currentDialects : []);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleSubmit = async () => {
    trackButtonClickGA("submit-get-details-button");

    if (selectedLanguages.length === 0) {
      toast({
        title: "Please select a language.",
        description: "You need to select a language to proceed forward.",
        status: "warning",
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    await updateUserProfile(
      selectedCountry,
      selectedLanguages,
      selectedGender,
      selectedAgeBucket,
      dialects
    );
    window.location.href = "/workspace";
  };

  return (
    <>
      {!loading && currentUserSettings && (
        <Container minW="35%" maxW="xl">
          <VStack className="pb-44 pt-14" spacing="2rem" align="start">
            <Text className="mx-auto text-3xl font-bold text-blue-900 md:text-6xl">
              Just one step more...
            </Text>

            <VStack spacing={0} align="start" minW="100%">
              <Text className="font-medium text-gray-700">
                Select the country you currently reside in
              </Text>
              <SingleSelectDropdown
                entity="Country"
                options={countryList}
                onChange={setSelectedCountry}
                currentValue={currentUserSettings.country_code}
              />
            </VStack>

            <VStack spacing={0} align="start">
              <Text className="font-medium text-gray-700">
                Select the languages you are comfortable giving feedback on. You
                should have good written fluency in the languages you specify.
              </Text>
              <MultiSelectDropdown
                entity="Language"
                options={languageList}
                onChange={setSelectedLanguages}
                currentValues={currentUserSettings.language_codes}
              />
            </VStack>

            <VStack spacing={0} align="start" minW="100%">
              <Text className="font-medium text-gray-700">Gender</Text>
              <SingleSelectDropdown
                entity="Gender"
                options={genderList}
                onChange={setSelectedGender}
                currentValue={currentUserSettings.gender}
              />
            </VStack>

            <VStack spacing={0} align="start" minW="100%">
              <Text className="font-medium text-gray-700">Age Range</Text>
              <SingleSelectDropdown
                entity="Age Range"
                options={ageGroupList}
                onChange={setSelectedAgeBucket}
                currentValue={currentUserSettings.age_range}
              />
            </VStack>

            <VStack spacing={0} align="start" minW="100%">
              <Text className="font-medium text-gray-700">
                Self report dialect
              </Text>
              <DialectInput dialects={dialects} setDialects={setDialects} />
            </VStack>

            <Center w="100%">
              <Button
                colorScheme="blue"
                onClick={handleSubmit}
                className="mx-auto"
              >
                Submit
              </Button>
            </Center>
          </VStack>
        </Container>
      )}
    </>
  );
}

export default GetDetails;
