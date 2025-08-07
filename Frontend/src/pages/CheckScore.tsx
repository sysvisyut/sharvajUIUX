import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
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
  educationLevel: string;
  
  // Employment & Income
  employmentType: string;
  monthlyIncome: string;
  yearsAtCurrentJob: string;
  
  // Housing
  monthlyHousingCost: string;
  hasMortgage: string;
  bankBalance: string;
  monthlySavings: string;
  
  // Family & Dependents
  numberOfDependents: string;
  
  // Credit & Loans
  numberOfCreditCards: string;
  hasStudentLoan: string;
  studentLoanPayment: string;
  hasCarLoan: string;
  carLoanPayment: string;
  
  // Credit Behavior
  recentCreditInquiries: string;
  latePayments: string;
  bankruptcyHistory: string;
  yearsOfCreditHistory: string;
}

const CheckScore = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<FormData>({
    age: '',
    state: '',
    educationLevel: '',
    employmentType: '',
    monthlyIncome: '',
    yearsAtCurrentJob: '',
    monthlyHousingCost: '',
    hasMortgage: '',
    bankBalance: '',
    monthlySavings: '',
    numberOfDependents: '',
    numberOfCreditCards: '',
    hasStudentLoan: '',
    studentLoanPayment: '',
    hasCarLoan: '',
    carLoanPayment: '',
    recentCreditInquiries: '',
    latePayments: '',
    bankruptcyHistory: '',
    yearsOfCreditHistory: ''
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
      fields: ['age', 'state', 'educationLevel']
    },
    {
      title: "Employment & Income",
      icon: Briefcase,
      fields: ['employmentType', 'monthlyIncome', 'yearsAtCurrentJob']
    },
    {
      title: "Housing",
      icon: Home,
      fields: ['monthlyHousingCost', 'hasMortgage', 'bankBalance', 'monthlySavings']
    },
    {
      title: "Family & Dependents",
      icon: Users,
      fields: ['numberOfDependents']
    },
    {
      title: "Credit & Loans",
      icon: CreditCard,
      fields: ['numberOfCreditCards', 'hasStudentLoan', 'studentLoanPayment', 'hasCarLoan', 'carLoanPayment']
    },
    {
      title: "Credit Behavior",
      icon: TrendingUp,
      fields: ['recentCreditInquiries', 'latePayments', 'bankruptcyHistory', 'yearsOfCreditHistory']
    }
  ];

  const stateOptions = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", 
    "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", 
    "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", 
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", 
    "Uttarakhand", "West Bengal", "Delhi"
  ];

  const educationOptions = [
    "High School", "Diploma", "Bachelor's", "Master's", "PhD", "Professional Degree"
  ];

  const employmentOptions = [
    "Salaried", "Self-employed", "Business Owner", "Freelancer", "Unemployed", "Student", "Retired"
  ];

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
                  {/* Personal Information Section */}
                  {currentSection === 0 && (
                    <motion.div
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.6 }}
                      className="space-y-6"
                    >
                      {/* Age */}
                      <div className="space-y-2">
                        <Label className="text-white font-cred-body font-medium tracking-wide">
                          AGE
                        </Label>
                        <Input
                          type="number"
                          value={formData.age}
                          onChange={(e) => handleInputChange('age', e.target.value)}
                          className="bg-black/20 border-white/20 text-white placeholder:text-white/40 focus:border-neon-blue focus:ring-neon-blue/20 font-cred-body"
                          placeholder="Enter your age"
                          min="18"
                          max="100"
                        />
                      </div>

                      {/* State */}
                      <div className="space-y-2">
                        <Label className="text-white font-cred-body font-medium tracking-wide">
                          STATE
                        </Label>
                        <Select value={formData.state} onValueChange={(value) => handleInputChange('state', value)}>
                          <SelectTrigger className="bg-black/20 border-white/20 text-white focus:border-neon-blue focus:ring-neon-blue/20 font-cred-body">
                            <SelectValue placeholder="Select your state" />
                          </SelectTrigger>
                          <SelectContent className="bg-black/90 border-white/20 text-white">
                            {stateOptions.map((state) => (
                              <SelectItem key={state} value={state} className="focus:bg-white/10">
                                {state}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>

                      {/* Education Level */}
                      <div className="space-y-2">
                        <Label className="text-white font-cred-body font-medium tracking-wide">
                          EDUCATION LEVEL
                        </Label>
                        <Select value={formData.educationLevel} onValueChange={(value) => handleInputChange('educationLevel', value)}>
                          <SelectTrigger className="bg-black/20 border-white/20 text-white focus:border-neon-blue focus:ring-neon-blue/20 font-cred-body">
                            <SelectValue placeholder="Select your education level" />
                          </SelectTrigger>
                          <SelectContent className="bg-black/90 border-white/20 text-white">
                            {educationOptions.map((education) => (
                              <SelectItem key={education} value={education} className="focus:bg-white/10">
                                {education}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>
                    </motion.div>
                  )}

                  {/* Employment & Income Section */}
                  {currentSection === 1 && (
                    <motion.div
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.6 }}
                      className="space-y-6"
                    >
                      {/* Employment Type */}
                      <div className="space-y-2">
                        <Label className="text-white font-cred-body font-medium tracking-wide">
                          EMPLOYMENT TYPE
                        </Label>
                        <Select value={formData.employmentType} onValueChange={(value) => handleInputChange('employmentType', value)}>
                          <SelectTrigger className="bg-black/20 border-white/20 text-white focus:border-neon-blue focus:ring-neon-blue/20 font-cred-body">
                            <SelectValue placeholder="Select employment type" />
                          </SelectTrigger>
                          <SelectContent className="bg-black/90 border-white/20 text-white">
                            {employmentOptions.map((employment) => (
                              <SelectItem key={employment} value={employment} className="focus:bg-white/10">
                                {employment}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>

                      {/* Monthly Income */}
                      <div className="space-y-2">
                        <Label className="text-white font-cred-body font-medium tracking-wide">
                          MONTHLY INCOME (₹)
                        </Label>
                        <Input
                          type="number"
                          value={formData.monthlyIncome}
                          onChange={(e) => handleInputChange('monthlyIncome', e.target.value)}
                          className="bg-black/20 border-white/20 text-white placeholder:text-white/40 focus:border-neon-blue focus:ring-neon-blue/20 font-cred-body"
                          placeholder="Enter monthly income"
                          min="0"
                        />
                      </div>

                      {/* Years at Current Job */}
                      <div className="space-y-2">
                        <Label className="text-white font-cred-body font-medium tracking-wide">
                          YEARS AT CURRENT JOB
                        </Label>
                        <Input
                          type="number"
                          value={formData.yearsAtCurrentJob}
                          onChange={(e) => handleInputChange('yearsAtCurrentJob', e.target.value)}
                          className="bg-black/20 border-white/20 text-white placeholder:text-white/40 focus:border-neon-blue focus:ring-neon-blue/20 font-cred-body"
                          placeholder="Enter years at current job"
                          min="0"
                          step="0.5"
                        />
                      </div>
                    </motion.div>
                  )}

                  {/* Housing Section */}
                  {currentSection === 2 && (
                    <motion.div
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.6 }}
                      className="space-y-6"
                    >
                      {/* Monthly Housing Cost */}
                      <div className="space-y-2">
                        <Label className="text-white font-cred-body font-medium tracking-wide">
                          MONTHLY HOUSING COST (₹)
                        </Label>
                        <Input
                          type="number"
                          value={formData.monthlyHousingCost}
                          onChange={(e) => handleInputChange('monthlyHousingCost', e.target.value)}
                          className="bg-black/20 border-white/20 text-white placeholder:text-white/40 focus:border-neon-blue focus:ring-neon-blue/20 font-cred-body"
                          placeholder="Enter monthly housing cost"
                          min="0"
                        />
                      </div>

                      {/* Has Mortgage */}
                      <div className="space-y-3">
                        <Label className="text-white font-cred-body font-medium tracking-wide">
                          HAS MORTGAGE?
                        </Label>
                        <RadioGroup
                          value={formData.hasMortgage}
                          onValueChange={(value) => handleInputChange('hasMortgage', value)}
                          className="flex space-x-6"
                        >
                          <div className="flex items-center space-x-2">
                            <RadioGroupItem value="yes" id="mortgage-yes" className="border-white/40 text-neon-blue" />
                            <Label htmlFor="mortgage-yes" className="text-white font-cred-body">Yes</Label>
                          </div>
                          <div className="flex items-center space-x-2">
                            <RadioGroupItem value="no" id="mortgage-no" className="border-white/40 text-neon-blue" />
                            <Label htmlFor="mortgage-no" className="text-white font-cred-body">No</Label>
                          </div>
                        </RadioGroup>
                      </div>

                      {/* Bank Balance */}
                      <div className="space-y-2">
                        <Label className="text-white font-cred-body font-medium tracking-wide">
                          BANK BALANCE (₹)
                        </Label>
                        <Input
                          type="number"
                          value={formData.bankBalance}
                          onChange={(e) => handleInputChange('bankBalance', e.target.value)}
                          className="bg-black/20 border-white/20 text-white placeholder:text-white/40 focus:border-neon-blue focus:ring-neon-blue/20 font-cred-body"
                          placeholder="Enter bank balance"
                          min="0"
                        />
                      </div>

                      {/* Monthly Savings */}
                      <div className="space-y-2">
                        <Label className="text-white font-cred-body font-medium tracking-wide">
                          MONTHLY SAVINGS (₹)
                        </Label>
                        <Input
                          type="number"
                          value={formData.monthlySavings}
                          onChange={(e) => handleInputChange('monthlySavings', e.target.value)}
                          className="bg-black/20 border-white/20 text-white placeholder:text-white/40 focus:border-neon-blue focus:ring-neon-blue/20 font-cred-body"
                          placeholder="Enter monthly savings"
                          min="0"
                        />
                      </div>
                    </motion.div>
                  )}

                  {/* Family & Dependents Section */}
                  {currentSection === 3 && (
                    <motion.div
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.6 }}
                      className="space-y-6"
                    >
                      {/* Number of Dependents */}
                      <div className="space-y-2">
                        <Label className="text-white font-cred-body font-medium tracking-wide">
                          NUMBER OF DEPENDENTS
                        </Label>
                        <Input
                          type="number"
                          value={formData.numberOfDependents}
                          onChange={(e) => handleInputChange('numberOfDependents', e.target.value)}
                          className="bg-black/20 border-white/20 text-white placeholder:text-white/40 focus:border-neon-blue focus:ring-neon-blue/20 font-cred-body"
                          placeholder="Enter number of dependents"
                          min="0"
                        />
                      </div>
                    </motion.div>
                  )}

                  {/* Credit & Loans Section */}
                  {currentSection === 4 && (
                    <motion.div
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.6 }}
                      className="space-y-6"
                    >
                      {/* Number of Credit Cards */}
                      <div className="space-y-2">
                        <Label className="text-white font-cred-body font-medium tracking-wide">
                          NUMBER OF CREDIT CARDS
                        </Label>
                        <Input
                          type="number"
                          value={formData.numberOfCreditCards}
                          onChange={(e) => handleInputChange('numberOfCreditCards', e.target.value)}
                          className="bg-black/20 border-white/20 text-white placeholder:text-white/40 focus:border-neon-blue focus:ring-neon-blue/20 font-cred-body"
                          placeholder="Enter number of credit cards"
                          min="0"
                        />
                      </div>

                      {/* Has Student Loan */}
                      <div className="space-y-3">
                        <Label className="text-white font-cred-body font-medium tracking-wide">
                          HAS STUDENT LOAN?
                        </Label>
                        <RadioGroup
                          value={formData.hasStudentLoan}
                          onValueChange={(value) => handleInputChange('hasStudentLoan', value)}
                          className="flex space-x-6"
                        >
                          <div className="flex items-center space-x-2">
                            <RadioGroupItem value="yes" id="student-loan-yes" className="border-white/40 text-neon-blue" />
                            <Label htmlFor="student-loan-yes" className="text-white font-cred-body">Yes</Label>
                          </div>
                          <div className="flex items-center space-x-2">
                            <RadioGroupItem value="no" id="student-loan-no" className="border-white/40 text-neon-blue" />
                            <Label htmlFor="student-loan-no" className="text-white font-cred-body">No</Label>
                          </div>
                        </RadioGroup>
                      </div>

                      {/* Student Loan Payment */}
                      {formData.hasStudentLoan === 'yes' && (
                        <div className="space-y-2">
                          <Label className="text-white font-cred-body font-medium tracking-wide">
                            STUDENT LOAN PAYMENT (₹)
                          </Label>
                          <Input
                            type="number"
                            value={formData.studentLoanPayment}
                            onChange={(e) => handleInputChange('studentLoanPayment', e.target.value)}
                            className="bg-black/20 border-white/20 text-white placeholder:text-white/40 focus:border-neon-blue focus:ring-neon-blue/20 font-cred-body"
                            placeholder="Enter monthly student loan payment"
                            min="0"
                          />
                        </div>
                      )}

                      {/* Has Car Loan */}
                      <div className="space-y-3">
                        <Label className="text-white font-cred-body font-medium tracking-wide">
                          HAS CAR LOAN?
                        </Label>
                        <RadioGroup
                          value={formData.hasCarLoan}
                          onValueChange={(value) => handleInputChange('hasCarLoan', value)}
                          className="flex space-x-6"
                        >
                          <div className="flex items-center space-x-2">
                            <RadioGroupItem value="yes" id="car-loan-yes" className="border-white/40 text-neon-blue" />
                            <Label htmlFor="car-loan-yes" className="text-white font-cred-body">Yes</Label>
                          </div>
                          <div className="flex items-center space-x-2">
                            <RadioGroupItem value="no" id="car-loan-no" className="border-white/40 text-neon-blue" />
                            <Label htmlFor="car-loan-no" className="text-white font-cred-body">No</Label>
                          </div>
                        </RadioGroup>
                      </div>

                      {/* Car Loan Payment */}
                      {formData.hasCarLoan === 'yes' && (
                        <div className="space-y-2">
                          <Label className="text-white font-cred-body font-medium tracking-wide">
                            CAR LOAN PAYMENT (₹)
                          </Label>
                          <Input
                            type="number"
                            value={formData.carLoanPayment}
                            onChange={(e) => handleInputChange('carLoanPayment', e.target.value)}
                            className="bg-black/20 border-white/20 text-white placeholder:text-white/40 focus:border-neon-blue focus:ring-neon-blue/20 font-cred-body"
                            placeholder="Enter monthly car loan payment"
                            min="0"
                          />
                        </div>
                      )}
                    </motion.div>
                  )}

                  {/* Credit Behavior Section */}
                  {currentSection === 5 && (
                    <motion.div
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.6 }}
                      className="space-y-6"
                    >
                      {/* Recent Credit Inquiries */}
                      <div className="space-y-2">
                        <Label className="text-white font-cred-body font-medium tracking-wide">
                          RECENT CREDIT INQUIRIES (LAST 6 MONTHS)
                        </Label>
                        <Input
                          type="number"
                          value={formData.recentCreditInquiries}
                          onChange={(e) => handleInputChange('recentCreditInquiries', e.target.value)}
                          className="bg-black/20 border-white/20 text-white placeholder:text-white/40 focus:border-neon-blue focus:ring-neon-blue/20 font-cred-body"
                          placeholder="Enter number of recent credit inquiries"
                          min="0"
                        />
                      </div>

                      {/* Late Payments */}
                      <div className="space-y-2">
                        <Label className="text-white font-cred-body font-medium tracking-wide">
                          LATE PAYMENTS IN LAST 12 MONTHS
                        </Label>
                        <Input
                          type="number"
                          value={formData.latePayments}
                          onChange={(e) => handleInputChange('latePayments', e.target.value)}
                          className="bg-black/20 border-white/20 text-white placeholder:text-white/40 focus:border-neon-blue focus:ring-neon-blue/20 font-cred-body"
                          placeholder="Enter number of late payments"
                          min="0"
                        />
                      </div>

                      {/* Bankruptcy History */}
                      <div className="space-y-3">
                        <Label className="text-white font-cred-body font-medium tracking-wide">
                          BANKRUPTCY HISTORY?
                        </Label>
                        <RadioGroup
                          value={formData.bankruptcyHistory}
                          onValueChange={(value) => handleInputChange('bankruptcyHistory', value)}
                          className="flex space-x-6"
                        >
                          <div className="flex items-center space-x-2">
                            <RadioGroupItem value="yes" id="bankruptcy-yes" className="border-white/40 text-neon-blue" />
                            <Label htmlFor="bankruptcy-yes" className="text-white font-cred-body">Yes</Label>
                          </div>
                          <div className="flex items-center space-x-2">
                            <RadioGroupItem value="no" id="bankruptcy-no" className="border-white/40 text-neon-blue" />
                            <Label htmlFor="bankruptcy-no" className="text-white font-cred-body">No</Label>
                          </div>
                        </RadioGroup>
                      </div>

                      {/* Years of Credit History */}
                      <div className="space-y-2">
                        <Label className="text-white font-cred-body font-medium tracking-wide">
                          YEARS OF CREDIT HISTORY
                        </Label>
                        <Input
                          type="number"
                          value={formData.yearsOfCreditHistory}
                          onChange={(e) => handleInputChange('yearsOfCreditHistory', e.target.value)}
                          className="bg-black/20 border-white/20 text-white placeholder:text-white/40 focus:border-neon-blue focus:ring-neon-blue/20 font-cred-body"
                          placeholder="Enter years of credit history"
                          min="0"
                          step="0.5"
                        />
                      </div>
                    </motion.div>
                  )}
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
    </div>
  );
};

export default CheckScore;
