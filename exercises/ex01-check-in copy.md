---
title: EX01 - Check-in for the Computer Science Experience Labs
author:
 - Kris Jordan
page: exercises
template: overview
---

In this exercise, you and a partner will create the front-end user interface for a simple check-in system for the UNC CS Experience Lab.

## Workflow Expectations

Pair Program, ideally in person, on stories A, B, and C. Do so in work-in-progress branches that get pushed to your team's repository and merged back into the main branch. Each member of the pair should be the commit author for at least one of the subtasks. You are encouraged to create a branch per story and a commit per subtask completion. Once all subtasks are complete, merge the story's commits back into `main`.

For Stories D and F, one partner should create a pull request for the completion of the story and the other should review it and merge it into `main` via GitHub's interface. Each partner should _at least_ create one pull request _and_ merge a pull request from the other partner. For reference on pull requests see [Creating a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) and [merging a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request).

## Deadlines

* Wednesday 2/1 - Stories A, B, and C
* Friday 2/3 - All Stories

---

## Personas

There are three personas for our user stories in this exercise.

Sol Student - Sol is a CS major who will visit and return to the CS Experience Lab as a productivity space.

Arden Ambassador - Arden is an ambassador to the CS Experience Lab who is volunteering at the check-in desk.

Merritt Manager - Merritt is a manager of the CS Experience Lab who evaluates usage of the space.

---

## Stories

### Story A

As any persona, I want to be able to click through to any of the story tasks below so that I can quickly navigate the application.

Subtasks:

1. All personas should find links to the routes which feature their stories on a home page URL path of "/" in the application. Clarification: Since there is no "user login" in this simple application, links to all stories will be presented to anyone using your application at this stage. Add links to the home page to each story's component as you implement it.

### Story B

As Sol Student, I want to register for the CS Experience Lab on my first visit to the colab space so that I can easily check-in in the future.

Subtasks:

1. Sol Student will find the navigation form at the URL path "/register".
2. Sol Student will need to register with their first name, last name, and PID.
3. Sol Student should see a thank-you message after registering that includes their name and the register form fields should be cleared.
4. Sol Student should have a link to return home after registration.

### Story C

As Merritt Manager, I want to be able to see a listing of all registered members.

Subtasks:

1. Merritt Manager will find these listings at the URL path "/stats".
2. Merritt Manager will see a list of registered members including their first and last names, and PID

Checkpoint A due Wednesday

### Story D

As Arden Ambassador, I want to be able to check Sol Student in using only thier PID so that I can easily check them in.

Subtasks:

1. Arden Ambassador will find the checkin form at the URL path "/checkin".
2. Arden Ambassador will need to enter a 9-digit PID. If the PID is not 9-digits exactly when the form is submitted, an error message should indicate bad PID. Additional note: barcode scanning is _not_ a part of this subtask or story.
3. After submitting the form, Arden Ambassador should see a message with the first and last name of the student who checked in. The 9-digit PID field should be cleared.
4. After submitting the form, if the 9-digit PID is not registered, Arden Ambassador should see a message letting them know the PID could not be found. The 9-digit PID field should not be cleared.

### Story E

As Merritt Manager, I want to be able to see a listing of all checkins.

Subtasks:

1. Merritt Manager will find these listings at the URL path "/stats".
2. Merritt Manager will see a list of registered members that is sorted by first name and includes their last name.
3. Merrit Manager will see a list of checkins that is sorted by the checking day and time and includes the checked in member's first and last name.

---

### Technical Requirements
1. Use separate components for Registration, Stats, and CheckIn user interfaces
2. Use services for Registrations and CheckIns. The Checkin service should depend on Registrations.

## Optional Challenges

 1. Make sure the user agrees to community standards in Subtask A.3.
 2. Validation of 9-digit PID
 3. Subtask A.4: Sol Student should not be able to register if their PID is already registered and should be presented with a message letting them know the PID is registered.
 4. Automatically redirect the user back to home after registration and check-in.
 5. Style the HTML using CSS to make it look _pretty_.
 6. Improve upon the HTML of the components with error messages contained in the page, with styling, rather than alerts.
 7. Create a child component for notifications (such as messages) that can be used in CheckIn and Registration.

## Getting Started

1. Find your Team Name and paired partner on the sheet linked to from the Canvas announcement.
2. Lookup their contact information in the [UNC Directory](https://directory.unc.edu) if you do not have it already.
3. E-mail them, if they have not e-mailed you already, and propose some of the next possible dates and times you can get together to pair program!
4. Accept the assignment on GitHub. First see if your team name already exists and join your teammate there, if so. If your team has not been accepted, create it with the exact same name shown on the EX01 Pairing sheet, and your partner will join your team later. PLEASE BE CAREFUL TO NAME YOUR TEAM CORRECTLY AND/OR JOIN THE CORRECT TEAM. The assignment link is here: <https://classroom.github.com/a/dwx9mnX5>
5. Wait until you can meet up with your pair partner to get started on the assignment so you can practice [pair programming](https://martinfowler.com/articles/on-pair-programming.html) together!
6. Once together, clone your repository.
7. Open your repository in VSCode and reopen it in a DevContainer.
8. Once inside the DevContainer, open a new terminal.
9. Change your working directory to `frontend`, where the Angular application is, in your Terminal.
10. Install 3rd party dependencies: `npm install`
11. After `npm install` completes successfully, you are encouraged to fully quit out of VSCode and reopen it. We have seen issues with the large number of `node_module` files causing issues without doing so after `npm install`.
12. Open a terminal back up, `cd frontend` again, and start the Angular development server as in the getting started tutorial.
13. From here, you should be able to open the application in the browser _and_ start working on implementing your first stories!

## Deploy Strategy, Configuration, and Submission

Let's get your project live on the internet! Until we learn about build processes and implementing our own containers and GitHub actions, we will take a simpler approach to deployment than is best practice.

### The general strategy will be as follows:

1. You will establish a separate branch, based off of `main`, for Github Pages deployment named `gh-pages`
2. When you want to deploy, you will locally switch to this branch, merge your `main` branch changes into it (this should always be a fast-forward, why?)
3. You will push your `gh-pages` branch to your team's GitHub repository.
4. Your GitHub repository will be configured to deploy to GitHub Pages (a Static HTML and Files service) based off of the `gh-pages` branch and, specifically, the `/docs` directory inside of it.
5. You will switch bach to `main` and continue working.

These steps are so mechanical, they could also be easily scripted in a shell file! For now, it's helpful to understand the process before automating and abstracting it away. Once you do, automation here would be a fun optional challenge!

### Configuration

We will make a configuration change while you are still on your `main` branch. Open `frontend/angular.json` and look in the sequence of object properties: `"projects" > "frontend" > "architect" > "build" > "options" > "outputPath"` and change this string to be `"../docs"`. When you build the project, which is a compilation process of sorts, it will emit the static, optimized files to this output path. We chose the directory `'docs'` in your repository because GitHub pages has a convention around using this directory name.

Go ahead and make a commit with just this configuration change and a message along the lines of "Configuring GitHub Pages Build."

Next, switch to a new branch named `gh-pages`.

Build your project with `ng build`. (Be sure your working directory is `frontend`.) Notice this created a directory named `docs` at the root of your project. If it didn't, go back and check your configuration.

Next, let's try using the [Caddy web server](https://caddyserver.com/), which is pre-installed in your DevContainer, to host the built project locally. This command expects you are still in the `frontend` working directory in your shell: 

`caddy file-server --root ../docs --listen :8080`

Now, open a browser to `localhost:8080` and you should see your built project. Note that if you make changes to your project they will not reload because this is a static, generated version of your project. You would need to rebuild; but we'll get to that. The whole point is we are building in preparation of deploying to the internet.

One key difference between running your project locally and running it on GitHub pages is that on GitHub pages, your project URL will be `<domain>/<project-repo-name>` whereas locally it is `localhost:8080/`. This difference in the "root" of your files being at `/` locally versus `/project-repo-name/` would take some extra configuration to replicate locally, so for now take it on trust that the steps you are about to take are based on expectations of GitHub pages. You can press `Ctrl+C` to signal for Caddy to stop.

Let's rebuild the project for your production environment with a custom `base-href`, which is required for your application to work with GitHub pages' URL structure. This is going to be based on the name of your repository on GitHub and will be important to get correct, so double check it. Open your team's repository on GitHub and grab your repository name. It should be something like: `ex01-checkin-team_XX`

Rebuild your angular project with a custom `base-href`: 

`ng build --base-href=/ex01-checkin-team_XX/`

Be sure to include the slashes and substitute the XX for your team name!

Add the files in your `docs` directory to a new commit and push your branch to GitHub: `git push origin gh-pages`

Back in GitHub, in your project's settings, go to `Pages` and under "Build and deployment" select "Deploy from a branch". Under branch, select your `gh-pages` branch. If it does not show up, go check previous steps. Then select your `/docs` directory. Save your changes.

The build and deploy to GitHub Pages can take a few minutes, but if you refresh after a minute or two you should see a message at the top saying: "Your site is live at URL" and be able to click the URL to see your built site live in production on GitHub Pages! You can send this to your mom!

If it doesn't work, you'll want to go back and confirm the build, commit, and push steps above. You can also try viewing the HTML of your index page on GitHub pages and looking for the `base` tag in the `head` section and being sure it is set to `/<your project name>/`. This is what gets configured during the build step with the `base-href` option above.

Once you have successfully built and deployed your site, all that is left to do is switch back to the `main` branch so you can continue work. If you want to publish in the future, your steps are:

1. Switch to the `gh-pages` branch.
2. Pull from the `gh-pages` branch to be sure you have any changes your teammate(s) may have made.
3. Merge in changes from your `main` branch.
4. Rebuild your project (be sure to set the base-href option!)
5. Make a commit with the updated files in your `docs` directory.
6. Push to your remote repository's `gh-pages` branch.
7. Switch back to `main` locally and keep on hacking!

**Caution**: Be careful to avoid building and committing while on the `main` branch. This will muddy up your repository. If you do, the best thing would be to delete those files and commit their deletion from the main branch.

**Best Practice**: Typically it is best practice _not_ to commit manually built files into a repository. Those are artifacts are best produced during an automated build process via a continuous integration system (such as GitHub Actions). However, setting up continuous integration systems is a large topic we'll explore later, so for now we are limiting the impact of these built files by using a separate branch to keep them cleanly tucked away in. You should be careful to avoid these files being added to your `main` branch!