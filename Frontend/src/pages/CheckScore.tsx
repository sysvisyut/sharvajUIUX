import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

import FloatingChatButton from '@/components/FloatingChatButton';
import {
  User,
  Briefcase,
  Home,
  Users,
  CreditCard,
  TrendingUp,
  Calculator,
  Star,
  Target
} from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import OrbBackground from '@/components/ui/OrbBackground';
import Navigation from '@/components/Navigation';

interface FormData {
  // Personal Information
  age: string;
  state: string;
  education_level: string;

  // Employment & Income
  employment_type: string;
  monthly_income: string;
  years_current_job: string;

  // Housing & Financial
  monthly_housing_cost: string;
  has_mortgage: string;
  bank_balance: string;
  monthly_savings: string;

  // Family
  num_dependents: string;

  // Credit & Loans
  num_credit_cards: string;
  has_student_loan: string;
  student_loan_payment: string;
  has_car_loan: string;
  car_loan_payment: string;

  // Credit History
  recent_credit_inquiries: string;
  late_payments_12m: string;
  bankruptcy_history: string;
  years_credit_history: string;
}

const CheckScore = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<FormData>({
    age: '',
    state: '',
    education_level: '',
    employment_type: '',
    monthly_income: '',
    years_current_job: '',
    monthly_housing_cost: '',
    has_mortgage: '',
    bank_balance: '',
    monthly_savings: '',
    num_dependents: '',
    num_credit_cards: '',
    has_student_loan: '',
    student_loan_payment: '',
    has_car_loan: '',
    car_loan_payment: '',
    recent_credit_inquiries: '',
    late_payments_12m: '',
    bankruptcy_history: '',
    years_credit_history: ''
  });

  const [currentSection, setCurrentSection] = useState(0);

  const handleInputChange = (field: keyof FormData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
    // Navigate to score result page
    navigate('/score-result');
  };

  const sections = [
    {
      title: "Personal Information",
      icon: User,
      fields: ['age', 'state', 'education_level']
    },
    {
      title: "Employment & Income",
      icon: Briefcase,
      fields: ['employment_type', 'monthly_income', 'years_current_job']
    },
    {
      title: "Housing & Financial",
      icon: Home,
      fields: ['monthly_housing_cost', 'has_mortgage', 'bank_balance', 'monthly_savings']
    },
    {
      title: "Family",
      icon: Users,
      fields: ['num_dependents']
    },
    {
      title: "Credit & Loans",
      icon: CreditCard,
      fields: ['num_credit_cards', 'has_student_loan', 'student_loan_payment', 'has_car_loan', 'car_loan_payment']
    },
    {
      title: "Credit History",
      icon: TrendingUp,
      fields: ['recent_credit_inquiries', 'late_payments_12m', 'bankruptcy_history', 'years_credit_history']
    }
  ];

  const stateOptions = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA",
    "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT",
    "VA", "WA", "WV", "WI", "WY", "DC"
  ];

  const educationOptions = [
    { value: "high_school", label: "High School" },
    { value: "some_college", label: "Some College" },
    { value: "bachelors", label: "Bachelor's Degree" },
    { value: "masters", label: "Master's Degree" },
    { value: "doctorate", label: "Doctorate/PhD" }
  ];

  const employmentOptions = [
    { value: "full_time", label: "Full Time" },
    { value: "part_time", label: "Part Time" },
    { value: "self_employed", label: "Self Employed" },
    { value: "unemployed", label: "Unemployed" },
    { value: "retired", label: "Retired" },
    { value: "student", label: "Student" }
  ];

  // Field configurations with human-friendly labels and examples
  const fieldConfig = {
    age: { label: "Age", placeholder: "e.g., 56", example: "56", type: "number" },
    state: { label: "State", placeholder: "Select your state", example: "TX", type: "select", options: stateOptions.map(s => ({ value: s, label: s })) },
    education_level: { label: "Education Level", placeholder: "Select education level", example: "masters", type: "select", options: educationOptions },
    employment_type: { label: "Employment Type", placeholder: "Select employment type", example: "full_time", type: "select", options: employmentOptions },
    monthly_income: { label: "Monthly Income ($)", placeholder: "e.g., 4842", example: "4842", type: "number" },
    monthly_housing_cost: { label: "Monthly Housing Cost ($)", placeholder: "e.g., 2096", example: "2096", type: "number" },
    num_dependents: { label: "Number of Dependents", placeholder: "e.g., 2", example: "2", type: "number" },
    years_current_job: { label: "Years at Current Job", placeholder: "e.g., 7", example: "7", type: "number" },
    num_credit_cards: { label: "Number of Credit Cards", placeholder: "e.g., 2", example: "2", type: "number" },
    has_student_loan: { label: "Have Student Loan?", placeholder: "Select", example: "Yes", type: "select", options: [{ value: "0", label: "No" }, { value: "1", label: "Yes" }] },
    student_loan_payment: { label: "Monthly Student Loan Payment ($)", placeholder: "e.g., 324", example: "324", type: "number" },
    has_car_loan: { label: "Have Car Loan?", placeholder: "Select", example: "Yes", type: "select", options: [{ value: "0", label: "No" }, { value: "1", label: "Yes" }] },
    car_loan_payment: { label: "Monthly Car Loan Payment ($)", placeholder: "e.g., 209", example: "209", type: "number" },
    has_mortgage: { label: "Have Mortgage?", placeholder: "Select", example: "No", type: "select", options: [{ value: "0", label: "No" }, { value: "1", label: "Yes" }] },
    bank_balance: { label: "Current Bank Balance ($)", placeholder: "e.g., 1309", example: "1309", type: "number" },
    monthly_savings: { label: "Monthly Savings ($)", placeholder: "e.g., 169", example: "169", type: "number" },
    recent_credit_inquiries: { label: "Recent Credit Inquiries (last 6 months)", placeholder: "e.g., 2", example: "2", type: "number" },
    late_payments_12m: { label: "Late Payments (last 12 months)", placeholder: "e.g., 1", example: "1", type: "number" },
    bankruptcy_history: { label: "Bankruptcy History", placeholder: "Select", example: "No", type: "select", options: [{ value: "0", label: "No" }, { value: "1", label: "Yes" }] },
    years_credit_history: { label: "Years of Credit History", placeholder: "e.g., 32", example: "32", type: "number" }
  };

  return (
    <div className="relative min-h-screen">
      <OrbBackground />
      <div className="fixed inset-0 bg-gradient-to-br from-black/20 via-transparent to-black/30 pointer-events-none -z-5"></div>
      
      <Navigation />
      
      <div className="pt-24 px-6 pb-12">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center mb-12"
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="flex justify-center mb-6"
            >
              <div className="w-20 h-20 bg-gradient-to-r from-neon-blue to-neon-purple rounded-3xl flex items-center justify-center glow-effect">
                <Calculator className="w-10 h-10 text-white" />
              </div>
            </motion.div>
            
            <h1 
              className="text-4xl md:text-5xl font-cred-heading font-bold text-white mb-4 tracking-tight uppercase"
              style={{ textShadow: '2px 2px 12px rgba(0, 0, 0, 0.8)' }}
            >
              Check Your Credit Score
            </h1>
            
            <p
              className="text-white/70 font-cred-body text-lg max-w-2xl mx-auto"
              style={{ textShadow: '1px 1px 6px rgba(0, 0, 0, 0.6)' }}
            >
              Get your personalized credit score based on alternative data and transparent scoring
            </p>
          </motion.div>

          {/* Progress Indicator */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="mb-8"
          >
            <div className="flex justify-center space-x-2 mb-4">
              {sections.map((_, index) => (
                <div
                  key={index}
                  className={`w-3 h-3 rounded-full transition-all duration-300 ${
                    index <= currentSection 
                      ? 'bg-gradient-to-r from-neon-blue to-neon-purple' 
                      : 'bg-white/20'
                  }`}
                />
              ))}
            </div>
            <p className="text-center text-white/60 font-cred-body text-sm">
              Step {currentSection + 1} of {sections.length}
            </p>
          </motion.div>

          {/* Form */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            <Card className="glass-effect border-white/10 glow-effect">
              <CardHeader className="text-center pb-6">
                <motion.div
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.6 }}
                  className="flex justify-center mb-4"
                >
                  {React.createElement(sections[currentSection].icon, {
                    className: "w-12 h-12 text-neon-blue"
                  })}
                </motion.div>
                
                <CardTitle 
                  className="text-2xl font-cred-heading font-bold text-white tracking-tight uppercase"
                  style={{ textShadow: '2px 2px 8px rgba(0, 0, 0, 0.8)' }}
                >
                  {sections[currentSection].title}
                </CardTitle>
              </CardHeader>

              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                  {/* Dynamic Form Sections */}
                  <motion.div
                    key={currentSection}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.6 }}
                    className="space-y-6"
                  >
                    {sections[currentSection].fields.map((fieldName) => {
                      const config = fieldConfig[fieldName as keyof typeof fieldConfig];
                      if (!config) return null;

                      return (
                        <div key={fieldName} className="space-y-2">
                          <Label className="text-white font-cred-body font-medium tracking-wide">
                            {config.label.toUpperCase()}
                            <span className="text-white/60 text-sm font-normal ml-2">
                              (Example: {config.example})
                            </span>
                          </Label>

                          {config.type === 'number' ? (
                            <Input
                              type="text"
                              value={formData[fieldName as keyof FormData]}
                              onChange={(e) => {
                                // Only allow numbers
                                const value = e.target.value.replace(/[^0-9]/g, '');
                                handleInputChange(fieldName as keyof FormData, value);
                              }}
                              className="bg-black/20 border-white/20 text-white placeholder:text-white/40 focus:border-neon-blue focus:ring-neon-blue/20 font-cred-body"
                              placeholder={config.placeholder}
                            />
                          ) : config.type === 'select' ? (
                            <Select
                              value={formData[fieldName as keyof FormData]}
                              onValueChange={(value) => handleInputChange(fieldName as keyof FormData, value)}
                            >
                              <SelectTrigger className="bg-black/20 border-white/20 text-white focus:border-neon-blue focus:ring-neon-blue/20 font-cred-body">
                                <SelectValue placeholder={config.placeholder} />
                              </SelectTrigger>
                              <SelectContent className="bg-black/90 border-white/20 text-white">
                                {(config as any).options?.map((option: any) => (
                                  <SelectItem key={option.value || option} value={option.value || option} className="focus:bg-white/10">
                                    {option.label || option}
                                  </SelectItem>
                                ))}
                              </SelectContent>
                            </Select>
                          ) : null}
                        </div>
                      );
                    })}
                  </motion.div>
                </form>

                {/* Navigation Buttons */}
                <div className="flex justify-between items-center mt-8 pt-6 border-t border-white/10">
                  <Button
                    type="button"
                    variant="ghost"
                    onClick={() => setCurrentSection(Math.max(0, currentSection - 1))}
                    disabled={currentSection === 0}
                    className="text-white hover:bg-white/10 nike-button font-cred-body disabled:opacity-50"
                  >
                    Previous
                  </Button>

                  {currentSection < sections.length - 1 ? (
                    <Button
                      type="button"
                      onClick={() => setCurrentSection(Math.min(sections.length - 1, currentSection + 1))}
                      className="bg-gradient-to-r from-neon-blue to-neon-purple hover:from-neon-purple hover:to-neon-pink text-white font-cred-heading font-bold px-6 py-3 tracking-wide uppercase nike-button"
                    >
                      Next
                    </Button>
                  ) : (
                    <Button
                      type="submit"
                      onClick={handleSubmit}
                      className="bg-gradient-to-r from-neon-blue to-neon-purple hover:from-neon-purple hover:to-neon-pink text-white font-cred-heading font-bold px-8 py-3 text-lg tracking-wide uppercase nike-button glow-effect"
                    >
                      <Target className="mr-2 w-5 h-5" />
                      Check My Score
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
      {/* Floating Chat Button */}
      <FloatingChatButton />
    </div>
  );
};

export default CheckScore;
