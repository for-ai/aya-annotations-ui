import axios from "axios";

import { getApiUrl } from "./config.jsx";

export const getTasks = async (userId, selectedLanguageUuid) => {
  try {
    const apiUrl = await getApiUrl();
    const response = await axios.get(
      `${apiUrl}/tasks/?user_id=${userId}&language_id=${selectedLanguageUuid}`
    );
    return response.data.tasks;
  } catch (error) {
    console.error(error);
    throw error;
  }
};

export const submitTaskAudit = async (taskData) => {
  try {
    const apiUrl = await getApiUrl();
    const response = await axios.post(`${apiUrl}/tasks/submit-audit`, taskData);
    return response;
  } catch (error) {
    console.error(error);
    throw error;
  }
};

export const submitTaskContribution = async (taskData) => {
  try {
    const apiUrl = await getApiUrl();
    const response = await axios.post(
      `${apiUrl}/tasks/submit-contribution`,
      taskData
    );
    return response;
  } catch (error) {
    console.error(error);
    throw error;
  }
};

export const submitTaskContributionAudit = async (taskData) => {
  try {
    const apiUrl = await getApiUrl();
    const response = await axios.post(
      `${apiUrl}/tasks/submit-contribution-audit`,
      taskData
    );
    return response;
  } catch (error) {
    console.error(error);
    throw error;
  }
};

export const getUserFeedbackTasks = async (userId, selectedLanguageUuid) => {
  try {
    const apiUrl = await getApiUrl();
    const response = await axios.get(
      `${apiUrl}/tasks/audits?user_id=${userId}&language_id=${selectedLanguageUuid}`
    );
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
};

export const submitTaskAuditContributionReview = async (taskData) => {
  try {
    console.log(taskData);
    const apiUrl = await getApiUrl();
    const response = await axios.post(
      `${apiUrl}/tasks/submit-contribution-audit-review`,
      taskData
    );
    return response;
  } catch (error) {
    console.error(error);
    throw error;
  }
};

export const submitTaskAuditReview = async (taskData) => {
  try {
    console.log(taskData);
    const apiUrl = await getApiUrl();
    const response = await axios.post(
      `${apiUrl}/tasks/submit-audit-review`,
      taskData
    );
    return response;
  } catch (error) {
    console.error(error);
    throw error;
  }
};
