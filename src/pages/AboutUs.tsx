import React from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Github, Linkedin, Mail, Users, LayoutDashboard } from 'lucide-react';
import { Link } from 'react-router-dom';

interface TeamMember {
  id: number;
  name: string;
  role: string;
  image: string;
  bio: string;
  isSupervisor?: boolean;
  links?: {
    github?: string;
    linkedin?: string;
    email?: string;
  };
}

const AboutUs: React.FC = () => {
  const teamMembers: TeamMember[] = [
    {
      id: 1,
      name: 'Prof. Hany Ammar',
      role: 'Project Supervisor',
      image: '/images/dr-hany.jpg', // ✅ Corrected
      bio: 'Leading the team with expertise in security and software engineering. Prof. Ammar brings years of academic and industry experience to guide the project vision.',
      isSupervisor: true,
      links: {
        email: 'ammar@example.com',
        linkedin: '#'
      }
    },
    {
      id: 2,
      name: 'Omar Husam',
      role: 'Project Lead',
      image: '/images/omar.jpg', // ✅ Corrected
      bio: 'Responsible for overall project coordination and technical architecture. Omar specializes in secure system design and cryptography implementation.',
      links: {
        github: '#',
        linkedin: '#',
        email: 'omar@example.com'
      }
    },
    {
      id: 3,
      name: 'Amr Mohamed',
      role: 'Frontend Developer',
      image: '/images/amr.jpg', // ✅ Corrected
      bio: 'Crafting the user interface with a focus on usability and accessibility. Amr is passionate about creating intuitive security tools for non-technical users.',
      links: {
        github: '#',
        linkedin: '#',
        email: 'amr@example.com'
      }
    },
    {
      id: 4,
      name: 'Marwan Mohamed',
      role: 'Security Specialist',
      image: '/images/marwan.jpg', // ✅ Corrected
      bio: 'Focused on encryption algorithms and detection patterns. Marwan ensures that the system provides reliable protection against evolving security threats.',
      links: {
        github: '#',
        linkedin: '#',
        email: 'marwan@example.com'
      }
    },
    {
      id: 5,
      name: 'Ahmed Ali',
      role: 'Backend Developer',
      image: '/images/ahmed.jpg', // ✅ Corrected
      bio: 'Building the robust backend infrastructure that powers our sensitive data detection engine. Ahmed specializes in scalable and secure API development.',
      links: {
        github: '#',
        linkedin: '#',
        email: 'ahmed@example.com'
      }
    },
  ];

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="flex flex-col items-center justify-center mb-12 text-center">
        <div className="flex items-center gap-2 mb-2">
          <Users className="h-6 w-6 text-primary" />
          <h1 className="text-3xl font-bold">Our Team</h1>
        </div>
        <p className="text-muted-foreground max-w-2xl">
          Meet the dedicated professionals behind TypeSecure — combining expertise in
          cybersecurity, software development, and user experience to create a comprehensive
          sensitive data protection solution.
        </p>
        <Link to="/dashboard" className="mt-4">
          <Button variant="outline" size="sm" className="gap-2">
            <LayoutDashboard className="h-4 w-4" /> Back to Dashboard
          </Button>
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
        {teamMembers
          .filter(member => member.isSupervisor)
          .map(member => (
            <Card 
              key={member.id} 
              className="col-span-full mx-auto max-w-md group hover:shadow-lg transition-all duration-300 border-primary/20"
            >
              <CardHeader className="text-center">
                <div className="w-32 h-32 mx-auto rounded-full overflow-hidden mb-4 border-4 border-primary/20 grayscale group-hover:grayscale-0 transition-all duration-500">
                  <img 
                    src={member.image} 
                    alt={member.name}
                    className="w-full h-full object-cover"
                  />
                </div>
                <Badge variant="outline" className="bg-primary/10 mb-2">
                  {member.isSupervisor ? 'Supervisor' : ''}
                </Badge>
                <CardTitle className="text-xl">{member.name}</CardTitle>
                <CardDescription>{member.role}</CardDescription>
              </CardHeader>
              <CardContent className="text-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <p className="text-sm text-muted-foreground">{member.bio}</p>
              </CardContent>
              <CardFooter className="flex justify-center space-x-4">
                {member.links?.email && (
                  <a href={`mailto:${member.links.email}`} className="text-muted-foreground hover:text-primary" aria-label="Email">
                    <Mail className="h-5 w-5" />
                  </a>
                )}
                {member.links?.linkedin && (
                  <a href={member.links.linkedin} className="text-muted-foreground hover:text-primary" aria-label="LinkedIn">
                    <Linkedin className="h-5 w-5" />
                  </a>
                )}
              </CardFooter>
            </Card>
          ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {teamMembers
          .filter(member => !member.isSupervisor)
          .map(member => (
            <Card key={member.id} className="group hover:scale-105 hover:shadow-lg transition-all duration-300">
              <CardHeader className="text-center">
                <div className="w-24 h-24 mx-auto rounded-full overflow-hidden mb-4 border-2 border-muted grayscale group-hover:grayscale-0 transition-all duration-500">
                  <img 
                    src={member.image} 
                    alt={member.name}
                    className="w-full h-full object-cover"
                  />
                </div>
                <CardTitle className="text-lg">{member.name}</CardTitle>
                <CardDescription>{member.role}</CardDescription>
              </CardHeader>
              <CardContent className="text-center h-24 overflow-hidden">
                <p className="text-sm text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  {member.bio}
                </p>
              </CardContent>
              <CardFooter className="flex justify-center space-x-4">
                {member.links?.github && (
                  <a href={member.links.github} className="text-muted-foreground hover:text-primary" aria-label="GitHub">
                    <Github className="h-4 w-4" />
                  </a>
                )}
                {member.links?.linkedin && (
                  <a href={member.links.linkedin} className="text-muted-foreground hover:text-primary" aria-label="LinkedIn">
                    <Linkedin className="h-4 w-4" />
                  </a>
                )}
                {member.links?.email && (
                  <a href={`mailto:${member.links.email}`} className="text-muted-foreground hover:text-primary" aria-label="Email">
                    <Mail className="h-4 w-4" />
                  </a>
                )}
              </CardFooter>
            </Card>
          ))}
      </div>
    </div>
  );
};

export default AboutUs;
