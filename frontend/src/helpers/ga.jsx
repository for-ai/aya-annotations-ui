import _ga from "../config/ga.jsx";

const _CATEGORIES = ["Button", "User"];

const _ACTIONS = ["Click", "Return", "New", "Add-details Abandoned"];

export const setAnalyticsUserId = async (userId) => {
  if (process.env.ENVIRONMENT === "production") {
    _ga.set({ userId });
  }
};

export const trackButtonClickGA = async (eventName) => {
  if (process.env.ENVIRONMENT === "production") {
    _ga.event({
      category: _CATEGORIES[0],
      action: _ACTIONS[0],
      label: eventName,
    });
  }
};

export const trackUserReturnGA = async () => {
  if (process.env.ENVIRONMENT === "production") {
    _ga.event({
      category: _CATEGORIES[1],
      action: _ACTIONS[1],
    });
  }
};

export const trackUserNewGA = async () => {
  if (process.env.ENVIRONMENT === "production") {
    _ga.event({
      category: _CATEGORIES[1],
      action: _ACTIONS[2],
    });
  }
};

export const trackUserAddDetailsAbandonedGA = async () => {
  if (process.env.ENVIRONMENT === "production") {
    _ga.event({
      category: _CATEGORIES[1],
      action: _ACTIONS[3],
    });
  }
};
