% ---------------------------------------------------------------------
% EG author guidelines plus sample file for EG publication using LaTeX2e input
% D.Fellner, v2.04, Dec 14, 2023


\title[Croissant Charts]%
     {Croissant Charts: Modulating the Performance of Normal Distribution Visualizations with Affordances}

% for anonymous conference submission please enter your SUBMISSION ID
% instead of the author's name (and leave the affiliation blank) !!
% for final version: please provide your *own* ORCID in the brackets following \orcid; see https://orcid.org/ for more details.
\author[Submission 1004]{Submission 1004}
% UNCOMMENT FROM HERE
\author[R. Fygenson, E. Bertini \& L. M. Padilla]
{\parbox{\textwidth}{\centering} R. Fygenson$^{1}$\orcid{0000-0002-0705-9000}, E. Bertini$^{1, 2}$\orcid{0000-0002-9932-0551}, and L. M. Padilla $^{1}$\orcid{0000-0001-9251-5279}
\\       
% For Computer Graphics Forum: Please use the abbreviation of your first name.
{\parbox{\textwidth}{\centering $^1$Khoury College of Computer Sciences, Northeastern University, Boston, MA, USA\\
$^2$College of Arts, Media and Design, Northeastern University, Boston, MA, USA}
}
}
% TO HERE ^^^^^^^^^^^^^^^^^^
% ------------------------------------------------------------------------

% if the Editors-in-Chief have given you the data, you may uncomment
% the following five lines and insert it here
%
% \volume{36}   % the volume in which the issue will be published;
% \issue{1}     % the issue number of the publication
% \pStartPage{1}      % set starting page


%-------------------------------------------------------------------------
\newcommand{\revi}[1]{\textcolor{black}{#1}}
  \newcommand{\rev}[1]{\textcolor{black}{#1}}
\newcommand{\pdf}[1]{\textcolor[HTML]{b5a50e}{\textbf{#1}}}
\newcommand{\qdp}[1]{\textcolor[HTML]{D1485B}{\textbf{#1}}}
\newcommand{\cten}[1]{\textcolor[HTML]{6B97A6}{\textbf{#1}}}
\newcommand{\ctw}[1]{\textcolor[HTML]{026494}{\textbf{#1}}}
\usepackage{float}
\usepackage{booktabs}
\usepackage{color,soul}
\usepackage[table, xcdraw]{xcolor}
\usepackage{amsmath}

\begin{document}
% \teaser{
%  \includegraphics[width=0.9\linewidth]{figs/teaser-1.pdf}
%  \centering
%   \caption{The three probability density function charts tested in the study, with annotations detailing their affordances as identified through qualitative evaluations.}
% \label{fig:teaser}
% }

\maketitle
%-------------------------------------------------------------------------
\begin{abstract}
   Affordances, originating in psychology, describe how an object’s design influences the physical and cognitive actions users may take. \rev{Past work applied affordance theory to visualization to explain how design decisions can impact the cognitive actions of visualization readers.} In this work, we demonstrate that affordances can complement effectiveness \revi{rankings} by further explaining the root causes behind visualizations’ task performance. To do so, we conduct a case study on \revi{static normal} probability density function plots, identifying their current affordances. Next, we \revi{identify} the optimal affordances for a common probability-comparison task and develop a novel affordance-driven visualization\revi{, the Croissant Chart, to support them.} We empirically validate the design's effectiveness through a preregistered study (\textit{n} = 808), demonstrating how affordances can inform predictable changes in task performance. Our findings underscore the potential for affordance-based approaches to enhance visualization effectiveness and inform future design decisions.

%  ACM CCS 1998
%  (see https://www.acm.org/publications/computing-classification-system/1998)
% \begin{classification} % according to https://www.acm.org/publications/computing-classification-system/1998
% \CCScat{Computer Graphics}{I.3.3}{Picture/Image Generation}{Line and curve generation}
% \end{classification}
   % (see https://www.acm.org/publications/class-2012)
%The tool at \url{http://dl.acm.org/ccs.cfm} can be used to generate
% CCS codes.
%Example:
\begin{CCSXML}
<ccs2012>
   <concept>
       <concept_id>10003120.10003145.10011769</concept_id>
       <concept_desc>Human-centered computing~Empirical studies in visualization</concept_desc>
       <concept_significance>500</concept_significance>
       </concept>
   <concept>
       <concept_id>10003120.10003145.10011770</concept_id>
       <concept_desc>Human-centered computing~Visualization design and evaluation methods</concept_desc>
       <concept_significance>300</concept_significance>
       </concept>
   <concept>
       <concept_id>10003120.10003145.10011768</concept_id>
       <concept_desc>Human-centered computing~Visualization theory, concepts and paradigms</concept_desc>
       <concept_significance>300</concept_significance>
       </concept>
 </ccs2012>
\end{CCSXML}

\ccsdesc[500]{Human-centered computing~Empirical studies in visualization}
\ccsdesc[300]{Human-centered computing~Visualization design and evaluation methods}
\ccsdesc[300]{Human-centered computing~Visualization theory, concepts and paradigms}


\printccsdesc   
\end{abstract}  
%-------------------------------------------------------------------------
\section{Introduction}
\label{sec:intro}
\textit{Affordance}, rooted in psychology, refers to the potential actions—both physical and mental—that users may take based on the design of an object \cite{hartson-1999-user-actionframework, gibson-ecological-vis-perception, Kaptelinin_aff_encyclo}. \revi{In the context of visualizations, \textit{mental actions} are the cognitive operations readers perform when interpreting a visualization, such as comparing values, grouping elements, or estimating trends. }
%Translating affordance theory to visualization research can help identify visualization designs' impact on the likelihood of communicating different information to readers.
\textit{\rev{Cognitive} affordances}, or the relationship between the design of an object and the knowledge that is imparted upon the object’s user~\cite{Hartson-2003}, can improve understanding of \revi{visualization} design implications by complementing task precision evaluations~\cite{fygenson-cog-affordance-framework}. % (see Quadri et al.'s work~\cite{quadri-perception-survey} for a review of evaluations), with investigations of the tasks that readers are \textit{most likely} to complete without explicit instruction \cite{fygenson2023affordances, xiong-grouping-cues, xiong-afford-comparison, xiong-reasoning-affordance, quadri-doyouseewhatisee, zacks-tversky-bars-lines, shah-graph-comprehension, stokes2025writerankratecomparing}. 
Because cognitive affordance offers an alternate lens of understanding how visualization designs impact mental actions, it can also \revi{suggest specific mental actions that} readers \revi{are likely to use}. In this paper, we demonstrate cognitive affordances\revi{' utility by using them to} connect visualization designs to readers' mental actions. \revi{This paper illustrates how} affordance-based visualization design can \revi{improve} task accuracy \revi{and} %We present a case study as initial evidence that cognitive affordances not only offer an alternate lens for evaluating visualizations but can also 
reveal the root cause of differences in task performance.

Although, affordances are well-studied in psychology and human\revi{-}computer interaction (HCI) (for a discussion, see~\cite{Kaptelinin_aff_encyclo}), they have only recently received attention in visualization research. %\rev{The majority of} past work that explicitly investigates affordances in visualization do\rev{es} so in the context of bar charts, finding that specific ordering and placement of bars can impact readers' data comparisons and takeaways \cite{xiong-afford-comparison, xiong-reasoning-affordance, fygenson2023affordances}.
Fygenson et al. translate affordance theory to visualization, characterizing cognitive affordances for visualization, summarizing related constructs, and proposing a framework to scaffold future research and discussion~\cite{fygenson-cog-affordance-framework}. %We build on this work by demonstrating cognitive affordances' utility in visualization evaluations and design processes, and \revi{by} establishing a foundation for future \revi{cognitive} affordance-based investigation.
We extend this work by applying cognitive affordances to visualization design and evaluation, laying the groundwork for future research.

To validate \revi{cognitive} affordances' utility, we demonstrate how they can support reasoning about likely causes of interpretation errors\revi{, such as} mathematically \textit{incorrect \revi{mental actions}}, and isolate specific elements of visualizations that are problematic. \revi{We then use} affordances to reason about design decisions that are likely to cue \textit{ideal \revi{mental actions}} for a task. %\revi{Because we investigate mental rather than physical actions, our experimental design does not require interactive stimuli, and can be used to investigate a wide variety of visualizations, including those that are static and not digital.}
We investigate \rev{affordances'} utility through a case study of \revi{static (i.e., non-interactive)} probability density function plots (PDFs). Prior research has identified systematic errors associated with \revi{static} PDF interpretation \cite{fygenson-padilla-pdf-scaling}, yet established methods for optimizing visualization design, such as the rankings of expressiveness and effectiveness \cite{munzner2015visualization}, have not been systematically applied to assess or improve PDFs. Moreover, established methods have not been used to assess alternative visualizations that are known to improve accuracy in probability-related tasks, such as quantile dot plots (QDPs) \cite{kay-qdps, fernandes2018-qdp-cdf}. %QDPs' performance improvement highlights the existence of designs and affordances that better support probabilistic reasoning than those currently found in PDFs. 
QDPs’ superior performance indicates that alternative affordances may better support probabilistic reasoning than PDFs. Through an affordance-based analysis of \revi{these non-interactive} visualizations, %\revi{we} aim to test design decisions that may reduce misinterpretations of PDFs and improve data comprehension. Specifically, 
we systematically examine how \rev{cognitive} affordances shape \revi{probability distribution} interpretation, offering the following key contributions:
\begin{itemize}
\item an analysis of PDF visualizations, demonstrating how an affordance\revi{s} can be used to redesign PDFs for a specific task%to improve the accuracy of their comparison
\item hypotheses about the underlying causes of \revi{a known} reasoning error with PDFs~\cite{fygenson-padilla-pdf-scaling} and predictions as to why these effects will not extend to QDPs
\item an affordance-based evaluation of cases where QDPs may \revi{lead to} interpretative challenges
\item a preregistered, empirical evaluation of the effectiveness of our redesigned PDFs, %\rev{(Fig. \ref{fig:teaser}, middle)}
traditional PDFs, and QDPs %rev{(Fig. \ref{fig:teaser}, left and right)}, 
\revi{that} link\revi{s} performance differences to our affordance-driven hypotheses
\end{itemize}
These contributions advance the understanding of how \rev{cognitive} affordances shape probabilistic reasoning.
%-------------------------------------------------------------------------
\section{Background}
\label{sec:background}
\subsection{Cognitive affordances in visualization}
\label{sec:cog-aff-theory}
\textbf{Theoretical foundation}. 
Ecological psychologist J.J. Gibson first introduced affordances in the late 1970s to define the relationship between an object and its user in terms of action possibilities (i.e., ways in which an individual could use an object)~\cite{gibson-ecological-vis-perception}. Over the following decades, researchers in HCI and psychology adopted affordances to describe how the shapes of physical items imply their possible and intended uses~\cite{norman-psych-of-everyday-things, norman-1999}, and later, how digital interfaces imply possible actions (e.g., clicking a button)~\cite{Kaptelinin_aff_encyclo}. \rev{Visualization research has investigated the affordances of user interactions, studying visual cues that incite users to hover over chart elements to reveal more information~\cite{boy-interactive-vis-aff}, and examining how users interact with dynamic physical bar charts~\cite{taher2015physicalaffbarchart}. However, this work does not apply to non-interactive charts, which comprise much visualized information~\cite{boy-interactive-vis-aff}.}%This work, however, is inapplicable to charts that are not interactive, which constitute a large portion of visualized information


 \rev{A recent subset of work investigates the non-physical affordances of visualizations, exploring how design impacts the cognitive actions of visualization readers, and thus the information that they are most likely to glean. Fygenson et al. provide an overview of this work, and name these non-physical affordances \textit{cognitive affordances}\cite{fygenson-cog-affordance-framework}. 
 They define cognitive affordances in visualization similarly to Norman’s affordance definition (i.e., all possible actions that a visualization’s design enables a reader to take)~\cite{norman-psych-of-everyday-things}, and specify that cognitive affordances are: (1) neither binary nor mutually exclusive, and (2) a factor of both a visualization's design and its reader.} \revi{Examples of cognitive actions that can be afforded include taking away messages about, and interpreting characteristics of, visualized data.}
They \revi{also} hypothesize that affordance-based evaluations can provide stronger logical reasoning for uncovering the root cause of misleading designs and suggesting successful alternatives. \revi{In this paper, we present an } %A major contribution of the present work is its 
initial validation of \revi{their} hypothesis. %that affordances can inform intentional visualization redesigns.

\noindent\textbf{Investigative methods.}
Within visualization, the investigation of affordances, or affordance-related concepts, has been supported via several methods (for a review, see \cite{fygenson-cog-affordance-framework}). The most popular method \rev{is a free-response question in which participants are shown a visualization and asked} open-ended questions about what they see (e.g., ``describe in a sentence
what is shown'')~\cite{quadri-doyouseewhatisee, carswell-spontaneous-interpretation, shah-graph-comprehension, zacks-tversky-bars-lines}.  This method can be modified by scoping such questions to specific tasks~\cite{xiong-afford-comparison}, %as done by Xiong et al., when investigating comparisons in bar charts , 
or by restricting codes of interest when thematically coding collected responses~\cite{shah-1995-comprehending-line-graphs}. %, as done by Shah and Carpenter. %when investigating whether nominal, ordinal, or metric data characteristics are likely to be communicated \cite{shah-1995-comprehending-line-graphs}. %Researchers can also investigate affordances through \rev{an inverse set-up}, in which participants are given data as a table or text statement and asked to create a visualization to represent the data \cite{zacks-tversky-bars-lines}. This method is the least popular, perhaps because thematically coding visual outputs is a less established method. 
%Thirdly, researchers can explore affordances through a rank chart method, in which participants are shown a takeaway and an assortment of visualizations that all support the takeaway and asked to choose the visualization that best represents the takeaway \cite{fygenson2023affordances, xiong-afford-comparison, stokes2025writerankratecomparing}. Lastly, a rating construct strength method presents participants with a series of visualizations and asks them to rank each graph on a scale of how well it communicates a set of concepts (e.g., uncertainty, balance, completeness, rigidity) \cite{maceachren-semiotics, Ziemkiewicz-dynamics-2010}. These last two methods are confirmatory and restrict the scope of findings to support larger sample sizes, replicability, and increased statistical power~\cite{fygenson2023affordances}. \rev{In recently published work, Stokes et al. test methods of studying affordances with human coders and a large language model. In this work, Stokes et al. introduce other methods of evaluating affordances,  including a ranking conclusions method in which participants are shown a graph and a set of takeaways and asked to rank the them~\cite{stokes2025writerankratecomparing}.} 
In our pilot studies (Sec.~\ref{sec:pilot}) and affordance evaluation (Sec.~\ref{sec:exp-design} and \ref{sec:exp-analysis}), we employ the free-response technique because of its exploratory nature and conventional coding. 

\noindent\textbf{Effectiveness rankings.}
Visualization design decisions and pedagogy are often supported by \revi{frameworks} that rank marks and channels by their ability to precisely communicate encoded data~\cite{munzner2015visualization, ware-info-vis-book, heer-bostock-repr, cleveland_mcgill_2012, cleveland-mcgills-shape-param-graphs, isenberg-sys-review-vis-techniques}. Extensions of precision-focused work investigate effectiveness from similar performance-based lenses, including accurate recall~\cite{borkin-beyond-memorability}, and minimal response time~\cite{livingston-eval-multivar-vis, isenberg-sys-review-vis-techniques}. Effectiveness \revi{rankings} are useful in evaluating common charts (e.g., bar and pie charts) and have been translated into automatic chart recommendation systems~\cite{mackinlay-auto-design, besher-feiner-autovisual}. Effectiveness \revi{rankings describe} the encodings that most precisely support a task, but offer little guidance as to the tasks that unprompted readers are most likely to complete (i.e., cognitive affordances). Past work has found that task effectiveness can correlate with visualizations' cognitive fit (i.e., how well a visualization corresponds to readers' mental representations of information)~\cite{vessey-cog-fit, vessey-cog-fit-empirical-study}, suggesting a relationship between readers' \revi{mental actions}, visualizations' designs, and effectiveness. %Because affordances can influence readers' cognitive actions, and therefore their mental strategies, this past work provides precedent for the hypothesis that visualizations' cognitive affordances and performance \revi{may be} related.

\rev{The logical scaffolding of affordance-based investigations sets them apart from traditional performance evaluations by providing alternative diagnostic power. Response time and accuracy evaluations can illuminate a visualization’s poor performance and support \revi{its} redesign through frameworks such as the effectiveness and expressiveness rankings~\cite{munzner2015visualization}. Although these frameworks are useful, their guidance does not always increase visualizations' interpretability~\cite{bertini-all-chart-not-scatterplot}, or consistently change the information that readers are likely to glean. %While ease and likelihood may be connected, they are fundamentally different metrics and past work has shown that one is not always indicative of the other~\cite{fygenson2023affordances}. 
Cognitive affordances, on the other hand, \revi{can} provid\revi{e} logical conclusions about the underlying cause of correct or incorrect interpretations and, as we show in this paper, motivat\revi{e} redesigns that correlate with improved performance.} 

\noindent \textbf{Affording \revi{mental actions}.}
%Cognitive affordances in visualization describe the likely mental actions that a person may take when first reading a visualization~\cite{fygenson-cog-affordance-framework}. 
Low-level tasks, such as comparing the lengths of two shapes or reading an axis label, contribute to higher-level takeaways and decision-making~\cite{bongshin-lee-task-taxonomy, padilla2018decision}. \revi{By describing the probable} lower-level mental actions of \revi{visualization readers, cognitive affordances can shed light on the driving factors behind readers' interpretations.} For example, past research has investigated how bar chart affordances can inform the likelihood of comparative takeaways~\cite{fygenson2023affordances, xiong-afford-comparison, xiong-grouping-cues}, finding \revi{bar} placement can significantly change the comparisons and higher-level takeaways that readers report. Afforded cognitive actions can also drive readers' \revi{mental actions} when they encounter an unfamiliar graph. For example, if a reader sees a PDF for the first time, its continuous edge and aesthetic similarity to a line chart \revi{(see Fig.~\ref{fig:pdf-aff}, top)} may afford extracting height information \rev{as one would do when reading a line chart} (\revi{Fig.~\ref{fig:pdf-aff}, row a and b}). In turn, the reader might adopt a height-focused strategy and characterize the PDF by its maximum height. 

\subsection{Probability Density Visualizations}
\label{sec:prob-visualizations}
Communicating probabilities is a common requirement when disseminating experimental results~\cite{padilla2022know}, and %Advocacy against null hypothesis significance testing has strengthened the motivation for researchers to visualize probability distributions~\cite{dragicevic-stats-in-hci}. 
%\rev{Although several distributional visualizations do not fully eliminate reader judgments of dichotomous \textit{p}-values, they can reduce nonlinear drops in confidence that are indicative of a ``cliff effect'' in interpreting probabilities in comparison to traditional confidence interval annotations and textual \textit{p}-values~\cite{helske-dichotomous-vis}}. 
probability distributions can be visualized in numerous ways%(for review, see Padilla et al.'s work
~\cite{padilla_review2022}. Box plots, and confidence, standard deviation, and histogram intervals display key statistical properties of distributions through visual representations of summary statistics. Despite their long-standing popularity in scientific communication for both experts and the general public~\cite{van2019communicating, Ross-intro-stats}, these visualization methods do not display the entire shape of a distribution, leading to a loss of statistical detail~\cite{correll2014error}. Additionally, prior research finds that interval visualizations and box plots induce errors in which readers incorrectly assume that values inside visualized boundaries are more probable than those just outside the boundaries, thereby misinterpreting encoded \revi{probability}~\cite{correll2014error, joslyn2021}. Visualizations that fully encode distributions' shape instead of only showing key statistical metrics can lead to more correct conclusions~\cite{greis-uncertainty}.

Many visualizations that display distribution shape, such as PDFs, violin, raincloud, and ridgeline plots, encode probability as the area under a curve. However, unlike other Cartesian-coordinate plots, these visualizations' y-axis values do not readily communicate useful information \cite{Ross-intro-stats}. Instead, extracting cumulative probabilities (i.e., the probability of a random variable being above or below a threshold or between two bounding thresholds) from these charts requires finding the relevant slice of the area under the curve and calculating the percentage of total area under the curve that the slice occupies. This calculation can be challenging, especially when a distribution is not uniform and the areas in question are nonpolygonal~\cite{fygenson-padilla-pdf-scaling}.

Modern visualization designs, such as quantile dot plots (QDPs)~\cite{kay-qdps} and hypothetical outcome plots (HOPs)~\cite{hullman-hops}, seek to maintain the same communication of distribution shape as area-encoded visualizations, while also increasing audience understanding through the use of visual frequency framing \rev{(i.e.,} expressing probabilities as natural frequencies). This method of communicating odds, such as ``6 out of 100 times'' rather than ``6\%'',  can improve comprehension of \revi{odds} in textual contexts\cite{cosmides-tooby-frequency-framing}. Frequency framing has inspired the discrete communication of probability as counts of marks instead of continuous areas \rev{in QDPs and HOPs}~\cite{fernandes2018-qdp-cdf, hullman-hops}. \revi{Members of the general public} are more likely to correctly interpret frequency-framed visualizations than PDFs in specific contexts \cite{kay-qdps, fernandes2018-qdp-cdf, hullman-hops, kale2020-qdp}.
Although they communicate more information than interval visualizations\cite{padilla_review2022}, these discretized visualizations still sacrifice detail in exchange for facilitating human reasoning. HOPs, for example, rely on animation, making them unsuitable for nondigital formats and requiring more time to extract precise information~\cite{kay-qdps}. QDPs trade some statistical resolution by using discrete dots to encode continuous distributions. This limitation is particularly relevant in low (20)-quantile QDPs, which prior studies suggest are more effective than higher (100)-quantile versions~\cite{kay-qdps}.

\noindent\textbf{Equal-height scaling vs equal-area scaling.} Statistical plotting software typically defaults to generating equal-area PDFs, such that the area under each PDF curve occupies the same number of pixels. Because each of these areas equals 1 (i.e., 100\% probability), equal-area scaling ensures all PDFs have the same probability-to-pixel ratio, allowing simple area judgments to facilitate cumulative probability comparisons (see Fig.~\ref{fig:pdf-aff}, row c). However, for area-encoded distribution visualizations (e.g., PDFs, violin plots, ridgelines), equal-area scaling can cause occlusion when some distributions are much narrower (i.e., have lower standard deviation) than others \revi{(see Fig.~\ref{fig:why-squish}, a)}. Spacing PDFs to accommodate tall distributions can use substantial vertical space \revi{(Fig.~\ref{fig:why-squish}, b) which is often restrictive to authors working within page limits, so visualization authors may choose to scale PDFs to the same height to save space (Fig.~\ref{fig:why-squish}, c).} This equal-height option is not mathematically incorrect \revi{and is popular enough to be supported by} statistical plotting software (e.g., STAN bayesplot~\cite{bayesplot-r}, ggdist~\cite{ggdist}).  Still, past research establishes that equal-height PDFs lead to more incorrect judgments than equal-area PDFs, for \revi{members of the general public} making simple cumulative probability comparisons~\cite{fygenson-padilla-pdf-scaling}. 
\begin{figure}[t]
\centering  
    \includegraphics[width=\linewidth, alt={The task ``Which solute, if either, has a higher probability of being present at t or less ppm in the sampled seawater?'' is presented above two normal probability density functions with different spreads and the threshold t labeled on both their x-axes. Next, we visualize strategies we observed people using to complete this task and whether these strategies lead to correct answers for equal area and equal height PDFs. The 5 strategies are 1) comparing the height of PDFs at their peaks, 2) comparing the height of PDFs at the threshold t, 3) comparing the areas under the PDFs' curves to the left of threshold t, 4) comparing the spreads of the PDFs to the left of threshold t, and 5) comparing the slopes of the PDFs at threshold t. Strategy 1 and strategy 3 render correct comparisons for only equal area PDFs. All other strategies render incorrect comparisons.}]{figs/pdf-affordances-task.pdf}
    \vspace{-4mm}
    \caption{Top: The task we test. Bottom: PDFs' afforded \revi{mental actions} from our pilot study. Some actions yield correct results for equal-area PDFs (left), but not for equal-height PDFs (right). \revi{See Section~\ref{sec:pilot} for more detail.}}
    \label{fig:pdf-aff}
    \vspace{-8mm}
\end{figure}

Notably, the impact of equal-height scaling on other probability distribution visualizations remains unexplored. However, we hypothesize that visualizations relying on frequency framing may be more robust to scaling as they encourage \revi{mental actions} independent of mark height or area. Additionally, visualizations that inherently maintain constant height, such as interval plots and box plots, fall outside this discussion, as they naturally have equal heights.

\begin{figure}[t]
\centering  
    \includegraphics[width=0.9\linewidth, alt={}]{figs/why-squish.pdf}
    \vspace{-4mm}
    \caption{\revi{Why would someone scale PDFs to equal-heights? (a) different variances can cause overlap and occlusion (b) separating them requires more space (c) equal-height scaling yields a compact, statistically correct figure.}}
    \label{fig:why-squish}
    \vspace{-6mm}
\end{figure}

\section{Study Materials and Methods}
\label{sec:materials-methods}
Scaling pairs of PDF plots to equal heights decreases \revi{members of the general public}'s ability to compare the distributions' cumulative probability below a provided threshold (see Fig.~\ref{fig:pdf-aff})~\cite{fygenson-padilla-pdf-scaling}. Motivated by these results, we examine \revi{the utility of affordance theory}, as discussed in Section~\ref{sec:cog-aff-theory}, in 
\revi{evaluating equal-height PDFs and designing alternate visualizations}.
\revi{To do so, we proceeded in four stages. First, we analyzed pilot free-response data and relevant literature to identify possible cognitive affordances of PDFs and related distribution visualizations (Section~\ref{sec:pilot}). We assessed these cognitive affordances' alignment with the cumulative probability comparison task we investigate in our experiment. Second, we defined ideal affordances for the task and hypothesized which design features may better support them (Section~\ref{sec:redesign}). Third, we developed a novel, affordance-informed visualization to more strongly cue correct mental actions (Section~\ref{sec:redesign}). Finally, we preregistered and conducted an empirical study to test whether our predicted affordances correspond to measurable differences in task performance (Sections~\ref{sec:hyp} through~\ref{sec:exp-analysis}).}

\subsection{Affordances of probability density visualizations}
\label{sec:pilot}
\noindent\textbf{Pilot Data.} We collected pilot data to hypothesize about the affordances of different probability density visualizations by asking participants who completed simple tasks with normal probability visualizations\revi{, such as comparing the odds of two distributions,} to  ``please describe in as much detail as possible how [they] interpreted the graph and what strategies [they] used to answer the questions.'' We conducted these pilot studies via Prolific.com with participants \revi{who had Prolific approval rate over 90\%, resided in the U.S., were fluent in English, and over the age of 18 (291 female, 292 male, 14 non-binary/third gender, 4 did not report gender). These responses were between 5 and 278 words, with a median word length of 27 words.} These pilot studies allowed us to refine the measures for our main study and gain insights into afforded strategies for comparing distributions. \revi{We recruited 601 participants for the pilot study. Participants were randomly assigned to view either }normal PDFs (\textit{n} = 300) or normal QDPs (\textit{n }= 301).

We analyzed responses by thematically coding them to identify recurring concepts associated with each visualization. To do so, %The coding process was as follows: 
        (1) an author reviewed all responses, (2) responses were \revi{manually} grouped based on \revi{conceptual} similar \revi{in the reported} sentiments, and (3) overarching themes were identified within these groupings.    

\label{sec:pdf-aff}
\noindent\textbf{Affordances of PDFs.} To illustrate how affordance evaluations can support visualization redesigns, we selected a visualization-task use case that has been shown to lead to errors. \revi{Members of the general public} are consistently worse at comparing cumulative probabilities when using equal-height PDFs (see Fig.~\ref{fig:pdf-aff})~\cite{fygenson-padilla-pdf-scaling}. We investigated this visualization-task combination because it presents a clear judgment error, involves a sufficiently complex visualization to warrant redesign, and has alternative visualizations (e.g., QDPs) that have demonstrated high performance in other tasks. By focusing on a specific scaling issue, %we use affordances to identify reasoning errors and propose a novel design, 
we provide a case study that exhibits the process of using affordances and their generative potential.

Our thematic coding of pilot data identified several \revi{mental actions} that likely led to incorrect calculations. \revi{Some participants} reported  comparing the heights of the normal PDFs, either at their mean (see Fig.~\ref{fig:pdf-aff} row a) or at the threshold of a cumulative probability (row b). \textit{Height-comparing} could be driven by PDFs' visual similarity to line charts \revi{(see Fig.~\ref{fig:pdf-aff} top).}
Although this \revi{action} reflects an incorrect understanding of PDFs, it is worth noting that when PDFs are scaled to equal \textit{areas}, height comparison can still result in correct comparisons (Fig.~\ref{fig:pdf-aff} row a, left). When PDFs are scaled to equal \textit{heights} (Fig.~\ref{fig:pdf-aff} row a, right), however, height comparison no longer ensures accurate cumulative probability comparisons.

Participants' also compared partial areas that correlated with the threshold
(Fig.~\ref{fig:pdf-aff} row c). \textit{Area-comparing} can be afforded by participants' interpretation of the PDF as an area chart, and although closer to a ``correct'' mathematical understanding of PDFs, also only yields correct judgments when the charts are scaled to equal areas.

Lastly, participants compared overall PDF spread (Fig.~\ref{fig:pdf-aff} row d) and slope (row e). Both \revi{mental actions} commonly led to incorrect comparisons. Participants who used PDF spread reported wider graphs having higher probabilities for our task, even though the opposite is true. Participants who used slope comparisons also fell susceptible to incorrect interpretations, such as ``... whichever curve was more steep was normally the one with less probability,'' which is the opposite of the case. %, as seen in Fig.~\ref{fig:pdf-aff} row e. 
These \textit{shape-comparing} \revi{actions} are robust to equal scaling; y-axis scaling does not change spread or significantly alter comparisons of PDF slope. Still, they led to incorrect conclusions. In summary, the first phase of our affordance evaluation identified three primary \revi{mental actions} that contribute to reasoning errors with equal-height PDFs: height-comparing, area-comparing, and shape-comparing.
\begin{figure}[h!]
\centering  
    \includegraphics[width=0.68\linewidth, alt={}]{figs/qdp-affordances.pdf}
    \vspace{-1mm}
    \caption{\revi{QDPs' afforded mental actions from our pilot study.}}
    \label{fig:qdp-aff}
    \vspace{-5mm}
\end{figure}

\noindent\textbf{Affordances of QDPs.}
A review of QDP pilot data revealed one predominant afforded strategy. Participants often reported \textit{counting} and then comparing the number of dots on the right of the cumulative threshold for each QDP \revi{(Fig.~\ref{fig:qdp-aff}, top)}.
This strategy is robust to equal-height scaling because height manipulations do not affect dot counts (see Fig. ~\ref{fig:stimuli} \revi{for equal-height QDPs}). QDPs' strong counting affordance is indicative of their frequency-framed motivation, as participants interpreted each dot as part of a greater whole (e.g., 5 dots out of 10 total).

Additionally, some participants mentioned confusion when quantile dots did not align with an x-axis value of interest, indicating that they perceived each dot as a single probability, as opposed to an approximated continuous distribution \revi{(Fig.~\ref{fig:qdp-aff})}. This discrete interpretation can lead to erroneous conclusions, especially when distributions have wide spreads that lead to large spaces between dots. This affordance aligns with past research on the nature of individual areas (e.g., bar charts) affording \revi{readers to interpret data as discrete} and connected dots (e.g., line charts) affording \revi{readers to interpret data as continuous} \cite{zacks-tversky-bars-lines, shah-graph-comprehension}. 

\noindent\textbf{Ideal affordances for equal-height PDFs.} After reviewing our pilot analysis, we identified ideal and undesired affordances from both PDFs and QDPs. Most significantly, QDPs afford counting, which makes them robust to equal-height scaling. PDFs lack this affordance, which we hypothesize contributes to incorrect judgments when scaled to equal heights (see Fig.~\ref{fig:pdf-aff}). However, QDPs also afford distributional discreteness much more than PDFs, which can lead to incorrect comparisons when two distributions share similar standard deviations (see Fig.~\ref{fig:cut-off-dist}). Thus, we identified that, for our cumulative probability task, an ideal visualization would afford both counting marks as parts of a whole and continuity. 

Next, we \revi{we constrained our design exploration to established static visualization techniques that have been empirically shown to support part-to-whole reasoning among members of the general public. Contemporary literature on part-to-whole and probability communication has strong empirical support for two approaches: icon arrays and treemaps. Icon arrays (i.e., frequency-framed displays) have been widely shown to improve probability comprehension by visually representing both the reference class and affected subset, thereby supporting accurate part–to-whole reasoning and reducing denominator neglect, especially among less numerate individuals (for reviews, see~\cite{ancker2006design, garcia2017designing}). Additionally, empirical work on rectangular treemaps suggests that spatial subdivision techniques can support accurate part–to-whole judgments. Although treemaps encode values using area, controlled experiments demonstrate judgment accuracy comparable to hierarchical bar charts at certain data densities and, in some cases, faster comparisons~\cite{kong2010perceptual}.} %searched for well-known visualization design choices that are classically used to communicate both counting parts of a greater whole, and continuity. 
\revi{Based on these prior works,} we identified two design choices that we hypothesized afforded counting parts of a whole: 
\begin{enumerate}
    \item an ``icon array'' technique in which colored glyphs are used to signal some items out of a larger set, as is done with QDPs, and
    \item a ``spatial subdivision'' technique in which a shape is divided by thin lines into smaller shapes, as in tree maps. 
\end{enumerate}

Of these two techniques, only the latter has the potential to afford continuity. Currently, this spatial subdivision technique communicates probability distributions through standard deviation or histogram intervals by encoding quantiles or standard deviations as abutting, equal-height bars~\cite{yang2023swaying, fernandes2018-qdp-cdf}. Although these charts are robust to vertical scaling and communicate a continuous distribution across a range of values, interval visualizations are susceptible to reasoning errors (for reviews see \cite{joslyn2021, padilla_review2022}) and are less ``expressive'' than alternative visualizations, which more readily communicate details of outliers and distribution shape~\cite{padilla_review2022}. Thus, we concluded that spatial subdivision is currently employed in charts that do not show the distributional information we desire.
% Surveying current chart designs, we recognized that histogram intervals use the spatial subdivision technique to communicate probability distributions (see Fig. SM4 Supplemental Materials). As noted in Section~\ref{sec:prob-visualizations}, however, we are interested in probability visualizations that maintain or extend PDFs' expressiveness and, therefore, are looking for designs that encode the mean, spread, and shape of their distributions. 

% \begin{figure}[t]
% \centering  
% \includegraphics[width=0.8\linewidth, alt={QDPs are often read by counting up each of their dots, which can communicate a part-to-whole relationship, and also a non-continuous range of probabilities (e.g., some 5\% chance at x = 1, 0\% chance at x = 1.5, 5\% chance at x = 2.}]{figs/qdp-affordances.pdf}
%     \caption{Affordances noted in our QDP pilot study. Top: counting individual dots. Bottom: discrete probabilities, such that some readers incorrectly interpret the gaps between columns of dots as showing zero probability.}
%     \label{fig:qdp-aff}
%     \vspace{-5mm}
% \end{figure}

% \begin{figure}[htb]
% \centering  
%     \includegraphics[width=.8\linewidth, alt={We juxtapose an icon array next to a QDP to show their use of similar encoding techniques. We do these same with a tree map and a pie chart  next to a histogram interval to show their similar encoding techniques.}]{figs/aff-part-to-whole.pdf}
%     \caption{Icon arrays (top left), and pie charts and tree maps (top right) both support frequency framing by affording a whole that is separated into countable parts. Their techniques can be translated to probability distribution visualizations (bottom).}
%         \label{fig:part-to-whole}
%         \vspace{-3mm}
% \end{figure}

 % Next, we reflected on probability distribution methods that use spatial subdivision to communicate parts-of-a-whole. We can see this technique in standard deviation or histogram intervals (Fig.~\ref{fig:part-to-whole}, bottom right), which typically form a stepped gradient by encoding quantiles or standard deviations as abutting bars~\cite{yang2023swaying, fernandes2018-qdp-cdf}. Although these charts are robust to vertical scaling and communicate a continuous distribution across a range of values, interval visualizations are susceptible to reasoning errors (for reviews see \cite{joslyn2021, padilla_review2022}) and are less ``expressive'' than alternative visualizations, which more readily communicate details of outliers and distribution shape~\cite{padilla_review2022}. From this reflection, we noted that spatial subdivision affords continuity but does not show the distributional information that we desired.

\subsection{An affordance-motivated redesign}
\label{sec:redesign}
Above, we established our goal of affording 1) counting dots as parts of a whole, 2) continuity, and 3) a general distributional shape to maintain expressiveness. % In Section~\ref{sec:aff-design-space}, we discussed design techniques and their respective affordances. 
Below, we present an affordance-informed redesign of PDFs: \textit{Croissant charts} (see Fig.~\ref{fig:anatomy}).


\begin{figure}[h!]
\centering  
\includegraphics[width=0.75\linewidth, alt={A croissant chart with annotations to describe how each design decisions impact the chart's affordances. All annotations are described in the caption.}]{figs/anatomy-croissant-pow.pdf}
    \caption{Croissant charts' intended affordances. PDF shape for expressiveness. Minimal slices with gaps afford continuity and parts of a whole. Dots afford counting and equality across slices.}
    \label{fig:anatomy}
    \vspace{-1mm}
\end{figure}

\noindent\textbf{Affording counting parts of a whole.} To afford counting strategies, we used two approaches: spatial subdivision and marks that encourage counting. %, and marks that suggest an equivalent area.
Subdivision cuts single shapes into multiple parts to communicate that the parts originate from one entity. Inspired by QDPs, we slice the PDF into quantiles, such that each slice represents an equal probability~\cite{kay-qdps}. However, we only display vertical slices to prevent the misinterpretation that horizontal slices of area under a PDF's curve lead to logical conclusions.

Additionally, we place a single dot in each quantile slice, in case QDPs' dots afford counting due to their shape. We also hypothesize that dots help mitigate the strong area, height, or width strategies we see in our pilot data on PDFs. We hypothesize that these dots correctly afford equal probabilities across each slice \rev{as a visual extrapolation of the equiprobability bias (i.e., people assume equal probabilities across items)%, even without indication of a uniform distribution)
~\cite{gauvrit-eqprob}. %In the case of croissant charts, 
We also use the dots to indicate equal probability in the charts' legend for added clarity. \revi{We darken the border of each section and each dot to increase their saliency at smaller scales.}}

\noindent\textbf{Affording a continuous distribution.}  To maintain perceptual continuity, we minimize area removal when subdividing the PDF. This decision draws on Gestalt principles of closure~\cite{wagemans-gestalt-perception}, and preserves as much of the PDF shape as possible. However, we include slight padding around each slice to ensure visual separation. 

\noindent\textbf{Affording general distributional shape.} To maintain the expressiveness with which PDFs display distributional shapes, we retain their density function curve rather than making each quantile the same height as in interval plots, or adopting a discretized distribution shape as in QDPs. We observed in pilot data that dots placed in QDPs' tails can skew readers' perception of a distribution's continuity and sometimes afford multimodality. Additionally, past research shows that bin width and dot size can influence the shape of QDPs~\cite{correll-prob-density2019}. By preserving the continuous shape of PDFs, we aimed for greater resilience against these distortions. 

\subsection{Investigative Questions and Hypotheses}
\label{sec:hyp}
We preregistered three main hypotheses about differences in reader performance when using PDFs, QDPs, and croissant charts on OSF. This preregistration \rev{and a visualization of our hypotheses for easier reference are available in Supplemental Materials\footnote{https://osf.io/txwj5/}.} The first hypothesis is that \textbf{(H1) equal-height PDFs will result in a lower likelihood of correct cumulative comparisons than equal-area PDFs}. This hypothesis is based on results from previous work \cite{fygenson-padilla-pdf-scaling}, and its confirmation would replicate prior findings while checking for methodological validity.
% \begin{figure}[t]
% \centering    \includegraphics[width=0.8\linewidth, alt={Hypotheses: H1) equal area PDFs will lead to higher likelihood of correct comparison than (i.e., ">") equal height PDFs. H2a) equal height Croissant-10s > equal height PDFs. H2b) equal height Croissant-20s > equal height PDFs. H2d) Scaling from equal area to equal height will decrease QDPs, Croissant-10s, and Croissant-20s' performance less than PDFs'. H3) Change in performance between 4.5 v 5 SD and other SD conditions in QDPs will be different than change in performance beteeen 4.5 v 5 SD and other SD conditions in Croissants and PDFs.}]{figs/hypotheses-table.pdf}
%     \caption{\rev{Visualizations of our preregistered hypotheses %for easier reference
%     }}
%     \label{fig:hyps}
%     \vspace{-8mm}
% \end{figure}

Our second \revi{set of} preregistered hypotheses examines whether visualizations that afford counting can mitigate the performance decline observed when PDFs are scaled to equal heights.
\revi{We preregistered four hypotheses concerning counting-affording designs. \textbf{Performance hypotheses:} We hypothesized that
\textbf{(H2a)} equal-height Croissant-10s,
\textbf{(H2b)} equal-height Croissant-20s, and
\textbf{(H2c)} equal-height QDPs (20 quantiles)
would each result in a higher probability of correct cumulative comparisons than equal-height PDFs.} \revi{\textbf{Robustness-to-scaling hypothesis:} We further hypothesized that
\textbf{(H2d)} QDPs, Croissant-10s, and Croissant-20s would exhibit a smaller decrease in correctness when moving from equal-area to equal-height scaling than PDFs.}

%Specifically, we hypothesized that \textbf{(H2a) equal-height croissants divided into 10 quantiles (Croissant-10s), (H2b) equal-height croissants divided into 20 quantiles (Croissant-20s), and (H2c) equal-height QDPs divided into 20 quantiles would each result in a higher probability of correct comparisons than equal-height PDFs}. We also hypothesized \textbf{(H2d) that QDPs, Croissant-10s, and Croissant-20s will be less affected by equal height scaling than PDFs}, that is, decreases in correct judgments due to equal-height scaling will be less pronounced in QDPs and both croissant charts than in PDFs. 

%(i.e., there will be an interaction between visualization type and scaling).

Our last experimental hypothesis is motivated by our theorizing  that QDPs only weakly afford a continuous distribution. We preregistered that \textbf{(H3) QDPs' relationship between standard deviation (SD) pair comparisons and correctness will differ from other visualizations' relationship between SD and correctness, specifically in the 4.5 vs. 5 SD condition}. In other words, QDPs' performance would drastically change in the 4.5 v 5 SD condition in a way that other visualizations' performance would not. We rationalized that when two distributions' SDs are similar, their QDPs' dots will be stacked similarly and moved only slightly along the x-axis in ways that may be too subtle for readers to recognize.

\subsection{Stimuli}
\label{sec:stimuli}
When comparing of cumulative probabilities of equal-area PDFs, readers can rely on heuristics, such as PDF height, to make accurate judgments. For equal-height PDFs, however, height comparison can lead to incorrect conclusions; other strategies, such as counting, offer a more robust approach. Following our affordance analysis of PDFs, we tested three types of visualizations: PDFs, which our pilot data suggest strongly afford continuity but only weakly afford counting, QDPs; which our pilot data suggest strongly afford counting but weakly afford distribution continuity; and croissant charts, which we designed to afford both continuity and counting.

We test QDPs with 20 quantiles because they have been shown to result in better performance than their 100-quantile counterparts \cite{kay-qdps}. We test croissant charts with 20 quantiles (Croissant-20s), as mathematical equivalents to our QDP stimuli, and croissant charts with 10 quantiles (Croissant-10s). Our pilot data showed that Croissant-10s outperform croissants with five quantiles, so we wanted to study how Croissant-10s compare to Croissant-20s.   

For all four graphs (PDFs, QDPs, Croissant-20s, and Croissant-10s), we created stimuli with two normal probability distributions stacked vertically (as shown in Fig.~\ref{fig:pdf-aff}, top). These stimuli were then scaled to either ``equal area'' or ``equal height'' (see Fig.~\ref{fig:stimuli}, left panel). For PDFs and both croissants ``equal area'' meant that the area below the two curves had the same number of pixels, and ``equal height'' meant that the distance from the highest point on the curve to the x-axis was held constant. For QDPs, ``equal area'' ensured that both graphs' dots were the same pixel size, while ``equal height'' maintained a constant distance from the top of the highest dot to the x-axis. In narrower distributions, this adjustment reduced dots' diameter to preserve their circular shape.

For each of our \revi{eight} stimuli types, we created four sets of distributions with varying SDs (see Fig.~\ref{fig:stimuli}, right panel). The first set presented a distribution with an SD of 2 and a distribution with an SD of 5. The rest compared distributions with SDs of 3 and 5, 4 and 5, and finally 4.5 and 5. We chose the first three of these SD comparisons because they were shown to have varying performance in previous work \cite{fygenson-padilla-pdf-scaling}. We added the 4.5 vs. 5 SD comparison, because we believed it could highlight QDPs' weaker affordance of a continuous distribution, as explained in H3 in Section~\ref{sec:hyp}. For each of the SD combinations we created two sets of stimuli, such that the vertical position of the narrower (higher SD) distribution was counterbalanced (see Fig.~\ref{fig:stimuli}, bottom right). This resulted in eight stimuli of each scaled visualization, for a total of 64 tested stimuli. We created all stimuli via custom D3.js functions, and edited (e.g., scaled, relabeled, etc.) them in Adobe Illustrator. Stimuli and generating scripts are available in Supplemental Materials.


\begin{figure}[h]
\centering   
\includegraphics[width=\linewidth, alt={Stimuli variations. All variations and labels are described in the caption.}]{figs/stimuli-overview-col.pdf}
\vspace{-2mm}
    \caption{%Experimental design illustrating between-subject (left panel) and within-subject (right panel) manipulations. 
    Stimuli overview. Left: Between-subjects; different visualization techniques (PDF, QDP, Croissant-10, Croissant-20) under two scaling conditions (Equal Area, Equal Height). Right: within-subjects; standard deviation pairs and position variations.}
    \label{fig:stimuli}
    \vspace{-4mm}
\end{figure}

\subsection{Experimental Design}
\label{sec:exp-design}
We designed a 4 (\textit{Visualization}) × 2 (\textit{Scaling}) × 4 (\textit{SD Pairs}) × 2 (\textit{Position}) mixed-subjects design \revi{(see Figure~\ref{fig:stimuli}).} The between-subjects variables were \textit{Visualization} and \textit{Scaling}. The within-subject variable of interest was \textit{SD Pairs}. We included \textit{Position} to counterbalance our stimuli and increase statistical power. We did not hypothesize about \textit{Position}'s impact, and included it as a covariate in our analysis. 
We investigated task correctness and collected participants' qualitative responses to observe afforded strategies.

\subsection{Participants}
We recruited U.S.-based participants over 18 through Prolific~\cite{prolific}, which anonymizes, qualifies, enrolls, and compensates participants, enabling a double-blind study. 
As per our preregistered power analysis, we recruited 808 participants (\textit{n} = 101 per between-subject group). Because affordances depend on readers' individual characteristics~\cite{fygenson-cog-affordance-framework}, we crowdsourced responses from people with varying backgrounds. % and exposure to visualizations. 
To account for variance in visualization education, we collected participants' graph literacy scores using the Short Graph Literacy test~\cite{okan-sgl-2019}.

\subsection{Procedure}
\label{sec:procedure}
Participants were informed of the estimated duration and compensation (12 USD/hour) and consented to an IRB-approved form, after which they completed the study on Qualtrics~\cite{qualtrics}. First, participants read instructions and were informed of a scenario in which scientists are measuring the concentration of two different solutes in seawater. This scenario was identical to that used in previous PDF comparison work~\cite{fygenson-padilla-pdf-scaling}, and adapted from a study on HOPs~\cite{hullman-hops}. Then, participants \revi{were asked to answer} an initial attention check \revi{question to confirm they were reading the instructions. Next,} they were instructed to make the size of their browser window as large as possible and shown an annotated illustration of an example plot. Next, participants answered eight questions, one for each pair of charts. Following previously published procedures \cite{fygenson-padilla-pdf-scaling}, all the charts were presented in randomized order, and the questions read ``Which solute, if either, has a \textbf{higher probability} of being present at \textbf{X or less ppm} in the sampled seawater?'' where X was in the same position across all stimuli (at threshold \textit{t} in Figure~\ref{fig:pdf-aff}), but varied depending on the numbering of each stimulus's x-axis. Participants chose from three options (``solute A has a higher probability'', ``solute B has a higher probability,'' and ``neither solute A nor solute B has a higher probability''). The correct option was always the solute with a lower SD. This task does not represent the full range of probability distribution use cases, but allows us to investigate the extent to which affordances can impact strategies such that specific task performance is modulated.
After completing the chart comparison questions, participants used an open-ended text response to report their thought processes while reading the charts. Finally, participants completed Okan et al.'s Short Graph Literacy test~\cite{okan-sgl-2019}. %, and then self-reported their age and gender.
The survey and its stimuli are available in Supplemental Materials.

\subsection{Analysis}
\label{sec:exp-analysis}
We preregistered the binomial Bayesian model in~\autoref{eq:model1} with uninformative priors centered at 0 and a standard deviation of 2.5. We used R packages \textit{tidyr} v. 1.3.1 for data processing \cite{r-tidyr}, \textit{brms} v. 2.20.4 for Bayesian modeling \cite{r-brms}, and \textit{tidybayes} v. 3.0.6 for data processing and visualization \cite{r-tidybayes}. \revi{As denoted in Eq.~\ref{eq:model1}}, our model %includes two two-way interactions to investigate the impact of visualization, scaling, and SD pair on task performance. We assess 
assesses the variance in participants' binary correctness as explained by the interaction between \textit{Visualization} and \textit{Scaling}, and the interaction between \textit{Visualization} and \textit{SD Pair}, as well as their lower-order terms.  \revi{In this model, $p_i = P(Y_i = 1)$ represents the posterior probability that participant $i$ makes a correct comparison. Because we use a logit link, $\text{logit}(p_i) = \log\!\left(\frac{p_i}{1 - p_i}\right)$, all fixed-effect coefficients are estimated on the log-odds scale.} Variable levels are described in Sec.~\ref{sec:exp-design}. We also account for any variance explained by \textit{Position} and \textit{Graph Literacy}.
%Below is the model described in R-notation \rev{\cite{r-brms}}:
%\begin{equation}
%    \begin{aligned}
%    Binary\: Correctness \sim \: & Visualization \times Scaling\\
%    & + Visualization \times SD Pair\\
%    & + Position + Graph\: Literacy + (1|ID)
%  \end{aligned}
%  \label{eq:model1}
%\end{equation}  
\revi{
\begin{equation}
\begin{aligned}
Y_i &\sim \text{Bernoulli}(p_i) \\
\text{logit}(p_i) &= 
\beta_0 + \beta_1 \text{Visualization}_i + \beta_2 \text{Scaling}_i \\
&\quad + \beta_3 (\text{Visualization}_i \times \text{Scaling}_i)
+ \beta_4 \text{SDPair}_i \\
&\quad + \beta_5 (\text{Visualization}_i \times \text{SDPair}_i)
+ \beta_6 \text{Position}_i \\
&\quad + \beta_7 \text{GraphLiteracy}_i
+ u_{ID[i]}
\end{aligned}
\label{eq:model1}
\end{equation}}
We also conducted an exploratory analysis of each visualization's affordances. Two raters qualitatively coded participants' descriptions of their thought processes when completing the cumulative probability task. We then calculated the intraclass correlation (ICC) for each code, and the raters reconciled any codes that had an ICC 95\% confidence interval with a lower bound less than 0.6. %Qualitative coding open responses is the most common method used to investigate cognitive affordances in visualization~\cite{fygenson-cog-affordance-framework}.

\begin{figure}[t!]
\centering  
\includegraphics[width=0.85\linewidth, alt={Visualized posteriors of the numbers in Table 1. The x-axis indicates likelihood of correct comparison, and range from 0 (left) to 100 (right).}]{figs/fig-posteriors.pdf}
    \caption{\revi{Posteriors of Eq.~\ref{eq:model1} show that QDPs are robust to equal-height scaling and perform best across most conditions except the 4.5 v 5 SD comparison, where they perform the worst. Equal-height croissant charts outperform equal-height PDFs. Distributions show posterior predicted probabilities of correct responses, transformed from log-odds %to probability
    for interpretability. Black dots and lines show mean predicted probabilities %(i.e., estimated likelihood of percent correct). Black
    and 95\% credible intervals. %Higher values indicate better performance (greater likelihood of a correct response), and non-overlapping intervals suggest stronger evidence of differences between conditions.
    }}
    \label{fig:posteriors}
    \vspace{-9mm}
\end{figure}

\section{Experimental Results}
\label{sec:results}
Below, we describe the results from our analysis of binary task correctness, the results from our exploratory analysis of affordances, and the relationship between observed affordance and task correctness. As in our preregistered justification, we recruited 808 participants (\textit{n} = 101 for each between-subject group). 438 participants self-reported to not be men, with a mean age of 44.0 years (\textit{SD} = 15.4). The mean short graph literacy score was 2.3 of 4 (\textit{SD} = 1.1). \rev{Participants took an average of 11 minutes and 5 seconds (\textit{SD} = 7 min, 2 sec) to complete the survey.} %, and the average survey completion time and compensation was 11 minutes and 5.4 seconds and 12.00 USD /hour. 
As preregistered, we computed our model with and without participants who failed the attention check and performed a sensitivity analysis. There were no meaningful differences in the results between the two samples. For a large sample size and more conservative results, we report posteriors of the model that uses \revi{responses from participants who passed and those who failed the attention check}. 

\subsection{Task Performance: Investigating Hypotheses}
\label{sec:hyp-results}
We investigated the amount of variance in correct comparisons based on visualization, scaling, and SD pairs with the binomial model in Eq.~\ref{eq:model1}. As preregistered, we interpret interaction effects with credible intervals that exclude zero as accounting for meaningful variance in task correctness. We use the term ``meaningful'' instead of ``statistically significant'' to avoid implying a fixed decision threshold (e.g., \textit{p} < .05), as advised by Bayesian best practices \cite{kruschke2021bayesianreporting}. We ran our model with each combination of possible referents. 
All analyses are available in Supplemental Materials. 

To examine H1, if equal-height \pdf{PDFs} lead to meaningfully fewer correct comparisons than equal-area \pdf{PDFs}, we can look to \textit{Scaling}'s main effect when \textit{Visualization}'s referent is the \pdf{PDF} condition (row 1 in Table~\ref{tab:model1}). \textit{Scaling}'s credible interval does not include zero, indicating that scaling has a meaningful effect on \pdf{PDF} task performance. By visually examining the posteriors from this model (Fig.~\ref{fig:posteriors}), the results show that equal-height \pdf{PDFs} (colored yellow in rows with gray backgrounds) result in fewer correct answers than equal-area \pdf{PDFs} (yellow in rows with white backgrounds) across all SD Pairs. Thus, we accept H1, and present evidence for the reproducibility of results from Fygenson and Padilla \cite{fygenson-padilla-pdf-scaling}.

To examine H2a-d, how equal-height visualizations that afford counting impact task correctness in comparison to equal-height \pdf{PDFs}, we can refer to rows 5-16 in Table~\ref{tab:model1}. These rows show the main effects of \textit{Visualization} when the model is run with \pdf{PDF} as the referent. Equal-height \ctw{Croissant-20s} resulted in meaningfully improved task correctness in comparison to equal-height \pdf{PDFs} across all SD pairs (rows 9-12), leading us to accept H2b. Equal-height \qdp{QDPs} meaningfully improved task correctness compared to equal-height \pdf{PDFs} across all SD pairs (rows 5–7), except for the 4.5 vs. 5 pair, where \qdp{QDP} performance was meaningfully worse, as indicated by the sign change in the last three columns of row 8. These findings support the acceptance of H2c, contingent on the considerations outlined in H3. Equal-height \cten{Croissant-10s} resulted in meaningfully improved task correctness only over equal-height \pdf{PDFs} for SD pairs 2 vs. 5 and 4.5 vs. 5 (rows 13 and 16), leading us to partially accept hypothesis H2a. These results are also evident in Figure~\ref{fig:posteriors}'s gray-background rows, which show \pdf{PDFs} consistently trailing behind both \ctw{Croissant-20s} and \qdp{QDPs}. %Notably, in the bottom row, \qdp{QDPs} exhibit the lowest accuracy, meaningfully lower than both \pdf{PDFs} and croissants.

To directly investigate H2d--whether \qdp{QDPs}, \ctw{Croissant-20s}, and \cten{Croissant-10s} reduce performance differences between equal-area and equal-height scaling more effectively than \pdf{PDFs}--we can examine the interaction effects of \textit{Visualization} and \textit{Scaling} in rows 17-19 of Table~\ref{tab:model1}. The results indicate that \qdp{QDPs} meaningfully decrease the expected drop in performance associated with scaling from equal-area to equal-height in comparison to \pdf{PDFs} (row 17). However, \cten{Croissant-10s} and \ctw{Croissant-20s} show no meaningful difference in their interactions with \pdf{PDFs} (rows 18-19). We do not find evidence to support the hypothesis that \cten{Croissant-10s} and \ctw{-20s} can mitigate the performance drop associated with equal-height \pdf{PDFs}, and thus only partially accept H2d. %Still, equal-height \cten{Croissant-10s} and \ctw{-20s} meaningfully improve task performance in comparison to equal-height \pdf{PDFs} (rows 9-16). This improvement is evident in Figure~\ref{fig:posteriors}, where the gray rows show that \cten{Croissant-10s} and \ctw{Croissant-20s} consistently outperform \pdf{PDFs}. 

\begin{figure}[b]
\centering  
\vspace{-5mm}
\includegraphics[width=0.8\linewidth, alt={Equal height Croissant-10s encourage readers to interpret partial areas when the threshold t falls inside a quantile, as opposed to cleanly between two quantiles. Equal height QDPs do not encourage the interpretation of partial areas when they threshold t falls between two columns of dots, which can lead to incorrect distribution comparisons.}]{figs/interedge-interpolation.pdf}
\vspace{-2mm}
    \caption{\revi{Equal-height Croissant-10s and QDPs with an SD of 4.5 (tops) and an SD of 5 (bottoms).} Results show that Croissant-10s afford inter-edge interpolation much more than QDPs.}
    \label{fig:cut-off-dist}
    \vspace{-5mm}
\end{figure}

Lastly, to assess whether \qdp{QDPs} exhibit different task performance when comparing the 4.5 vs. 5 SD pair relative to other SD pairs, and if this performance differs from other visualizations%under the same SD pair comparisons
, we analyze the interaction between \textit{SD Pair} and \textit{Visualization}. Specifically, we examine meaningful differences when running the model with a \textit{Visualization} referent of \qdp{QDP} and \textit{SD Pair} referent of 4.5 vs. 5. Rows 20-28 in Table~\ref{tab:model1} show relevant model outputs and are all meaningfully different. A meaningful difference in QDP task performance across SD pairs is further supported by the last two rows of Figure~\ref{fig:posteriors}, where \qdp{QDPs} perform markedly worse than other charts. This drop in performance is notable because \qdp{QDPs} perform the best in all other conditions.  These findings lead us to accept (H3) that \qdp{QDPs}' relationship between task performance for 4.5 v 5 SD and any other SD pair is different from \pdf{PDFs}', \ctw{Croissant-20s}', and \cten{Croissant-10s}'. %More colloquially, this finding shows that QDPs lead to worse performance when used to compare distributions with 4.5 and 5 SDs than their performance when used to compare distributions with other SDs, and this decrease in performance is meaningfully worse than the decrease in performance that other tested visualizations experience.
To further analyze QDPs' performance %relative to the other visualizations 
in the 4.5 v 5 \textit{SD Pair} condition, we examine the main effect of \textit{Visualization} when the model's referents are set to \qdp{QDP},  4.5 vs. 5 SD, and first Equal Height, then Equal Area. Rows 32-37 in Table~\ref{tab:model1} show that \qdp{QDPs} perform meaningfully worse than \pdf{PDFs}, \ctw{Croissant-20s}, and \cten{Croissant-10s} when comparing a distribution with SD of 4.5 to a distribution with SD of 5, regardless of scaling.

In summary, our analysis reveals that equal-height \pdf{PDFs} lead to a lower likelihood of task correctness than equal-area \pdf{PDFs}, equal-height \ctw{Croissant-20s} improved chances of correctness over equal-height \pdf{PDFs}, although not as well as equal-height \qdp{QDPs}. \qdp{QDPs} were especially robust to scaling, and frequently outperformed other visualizations. However, \qdp{QDPs} led to meaningfully lower chances of correctly comparing distributions with SDs of 4.5 and 5, than all other visualizations. These findings highlight the benefits of \ctw{Croissant-20s} and \qdp{QDPs} over \pdf{PDFs}, while also demonstrating a specific weakness of low-quantile \qdp{QDPs}.
\vspace{-2mm}

\begin{table}[h!]
 \caption{%Rows show 95\% credible intervals in log odds. Darker cell backgrounds indicate stronger effects. 
  %  \revi{l-CI and u-CI indicate the lower and upper bounds of the credible interval, respectively. Cr-20 = Croissant-20, Cr-10 = Croissant-10.}
  \revi{Rows report posterior log-odds from Eq.~\protect{\ref{eq:model1}} contrasted between experimental conditions with 95\% Bayesian credible intervals. Darker cell backgrounds indicate stronger effects. l-CI and u-CI denote lower and upper bounds of credible intervals, respectively. Cr-20 = Croissant-20; Cr-10 = Croissant-10. Odds ratios are obtained by exponentiating the reported log-odds estimates.}
  }
    \vspace{-1mm}
    {\footnotesize
    \resizebox{\columnwidth}{!}{
    \begin{tabular}{@{}l@{\hspace{0.05cm}}c@{\hspace{0.15cm}}c@{\hspace{0.18cm}}c| l@{\hspace{0.2cm}}c@{\hspace{0.22cm}}c@{\hspace{0.15cm}}c@{}}
        \toprule
        \multicolumn{4}{c|}{Referent Conditions} & Comparison & Est\rev{imate} & \textbf{l-CI} & \textbf{u-CI} \\ 
        \midrule
         \textit{Row} & \textbf{Vis} & \textbf{SD Pair} & \textbf{Scaling} & & & & \\
        \midrule
        \textit{1} & PDF & N/A & Eq. Height & Eq. Area & \cellcolor[HTML]{DBE7F6}{1.26} & \cellcolor[HTML]{DBE7F6}0.78 & \colorbox[HTML]{DBE7F6}{1.75}\\
        \textit{2} & QDP & N/A & Eq. Height & Eq. Area & 0.11 & -0.37 & 0.61 \\
        \textit{3} & Cr-20 & N/A & Eq. Height & Eq. Area & \cellcolor[HTML]{EDF3FB}0.86 & \cellcolor[HTML]{EDF3FB}0.38 & \colorbox[HTML]{EDF3FB}{1.34}\\
        \textit{4} & Cr-10 & N/A & Eq. Height & Eq. Area & \cellcolor[HTML]{EDF3FB}{0.82} & \cellcolor[HTML]{EDF3FB}0.35 & \colorbox[HTML]{EDF3FB}{1.30}\\
        \midrule
        \textit{5} & PDF & 2 v 5 & Eq. Height & QDP & \cellcolor[HTML]{DBE7F6}1.80 & \cellcolor[HTML]{DBE7F6}1.24 & \colorbox[HTML]{DBE7F6}{2.37} \\
        \textit{6} & PDF & 3 v 5 & Eq. Height & QDP & \cellcolor[HTML]{C4DAF1}2.29 & \cellcolor[HTML]{C4DAF1}1.71 & \colorbox[HTML]{C4DAF1}{2.88} \\
        \textit{7} & PDF & 4 v 5 & Eq. Height & QDP & \cellcolor[HTML]{DBE7F6}1.45 & \cellcolor[HTML]{DBE7F6}0.88 & \colorbox[HTML]{DBE7F6}{2.02}\\
        \textit{8} & PDF & 4.5 v 5 & Eq. Height & QDP & \cellcolor[HTML]{EDF3FB}-0.99 & \cellcolor[HTML]{EDF3FB}-1.65 & \colorbox[HTML]{EDF3FB}{-0.34} \\
        \textit{9} & PDF & 2 v 5 & Eq. Height & Cr-20 & \cellcolor[HTML]{EDF3FB}0.88 & \cellcolor[HTML]{EDF3FB}0.32 & \colorbox[HTML]{EDF3FB}{1.45} \\
        \textit{10} & PDF & 3 v 5 & Eq. Height & Cr-20 & \cellcolor[HTML]{EDF3FB}0.71 & \cellcolor[HTML]{EDF3FB}0.15 & \colorbox[HTML]{EDF3FB}{1.28}\\
        \textit{11} & PDF & 4 v 5 & Eq. Height & Cr-20 & \cellcolor[HTML]{EDF3FB}0.77 & \cellcolor[HTML]{EDF3FB}0.21 & \colorbox[HTML]{EDF3FB}{1.33}\\
        \textit{12} & PDF & 4.5 v 5 & Eq. Height & Cr-20 & \cellcolor[HTML]{EDF3FB}0.90 & \cellcolor[HTML]{EDF3FB}0.32 & \colorbox[HTML]{EDF3FB}{1.49}\\
        \textit{13} & PDF & 2 v 5 & Eq. Height & Cr-10 & \cellcolor[HTML]{EDF3FB}0.69 & \cellcolor[HTML]{EDF3FB}0.13 & \colorbox[HTML]{EDF3FB}{1.25} \\
        \textit{14} & PDF & 3 v 5 & Eq. Height & Cr-10 & 0.49 & -0.06 & 1.05 \\
        \textit{15} & PDF & 4 v 5 & Eq. Height & Cr-10 & 0.34 & -0.22 & 0.89 \\
        \textit{16} & PDF & 4.5 v 5 & Eq. Height & Cr-10 & \cellcolor[HTML]{EDF3FB}0.60 & \cellcolor[HTML]{EDF3FB}0.02 & \colorbox[HTML]{EDF3FB}{1.19} \\
        \midrule
        \textit{17} & PDF & N/A & Eq. Height & QDP x Eq. Area & \cellcolor[HTML]{DBE7F6}-1.14 & \cellcolor[HTML]{DBE7F6}-1.83 & \colorbox[HTML]{DBE7F6}{-0.46} \\
        \textit{18} & PDF & N/A & Eq. Height & Cr-20 x Eq. Area & -0.40 & -1.09 & 0.27 \\
        \textit{19} & PDF & N/A & Eq. Height & Cr-10 x Eq. Area & -0.40 & -1.08 & 0.27 \\
        \midrule
        \textit{20} & QDP & 4.5 v 5 & N/A & PDF x 2 v 5 & \cellcolor[HTML]{C4DAF1}-2.61 & \cellcolor[HTML]{C4DAF1}-3.17 & \colorbox[HTML]{C4DAF1}{-2.05}\\
        \textit{21} & QDP & 4.5 v 5 & N/A & PDF x 3 v 5 & \cellcolor[HTML]{A5C8EA}-3.08 & \cellcolor[HTML]{A5C8EA}-3.66 & \colorbox[HTML]{A5C8EA}{-2.49}\\
        \textit{22} & QDP & 4.5 v 5 & N/A & PDF x 4 v 5 & \cellcolor[HTML]{C4DAF1}-2.24 & \cellcolor[HTML]{C4DAF1}-2.80 & \colorbox[HTML]{C4DAF1}{-1.69}\\
        \textit{23} & QDP & 4.5 v 5 & N/A & Cr-20 x 2 v 5 & \cellcolor[HTML]{C4DAF1}-2.58 & \cellcolor[HTML]{C4DAF1}-3.14 & \colorbox[HTML]{C4DAF1}{-2.04}\\
        \textit{24} & QDP & 4.5 v 5 & N/A & Cr-20 x 3 v 5 & \cellcolor[HTML]{A5C8EA}-3.24 & \cellcolor[HTML]{A5C8EA}-3.82 & \colorbox[HTML]{A5C8EA}{-2.66}\\
        \textit{25} & QDP & 4.5 v 5 & N/A & Cr-20 x 4 v 5 & \cellcolor[HTML]{C4DAF1}-2.35 & \cellcolor[HTML]{C4DAF1}-2.89 & \colorbox[HTML]{C4DAF1}{-1.79}\\
        \textit{26} & QDP & 4.5 v 5 & N/A & Cr-10 x 2 v 5 & \cellcolor[HTML]{C4DAF1}-2.47 & \cellcolor[HTML]{C4DAF1}-3.03 & \colorbox[HTML]{C4DAF1}{-1.92}\\
        \textit{27} & QDP & 4.5 v 5 & N/A & Cr-10 x 3 v 5 & \cellcolor[HTML]{A5C8EA}-3.15 & \cellcolor[HTML]{A5C8EA}-3.74 & \colorbox[HTML]{A5C8EA}{-2.58}\\
        \textit{28} & QDP & 4.5 v 5 & N/A & Cr-10 x 4 v 5 & \cellcolor[HTML]{C4DAF1}-2.48 & \cellcolor[HTML]{C4DAF1}-3.02 & \colorbox[HTML]{C4DAF1}{-1.94}\\
        \midrule
        \textit{29} & QDP & 4.5 v 5 & N/A & 2 v 5 & \cellcolor[HTML]{A5C8EA}3.86 & \cellcolor[HTML]{A5C8EA}3.43 & \colorbox[HTML]{A5C8EA}{4.31}\\
        \textit{30} & QDP & 4.5 v 5 & N/A & 3 v 5 & \cellcolor[HTML]{7BAFDB}4.73 & \cellcolor[HTML]{7BAFDB}4.27 & \colorbox[HTML]{7BAFDB}{5.21}\\
        \textit{31} & QDP & 4.5 v 5 & N/A & 4 v 5 & \cellcolor[HTML]{A5C8EA}3.43 & \cellcolor[HTML]{A5C8EA}3.02 & \colorbox[HTML]{A5C8EA}{3.87} \\
        \midrule
        \textit{32} & QDP & 4.5 v 5 & Eq. Area & PDF & \cellcolor[HTML]{DBE7F6}1.92 & \cellcolor[HTML]{DBE7F6}1.32 & \colorbox[HTML]{DBE7F6}{2.53}\\
        \textit{33} & QDP & 4.5 v 5 & Eq. Area & Cr-20 &\cellcolor[HTML]{C4DAF1} 2.39 & \cellcolor[HTML]{C4DAF1}1.79 & \colorbox[HTML]{C4DAF1}{3.00}\\
        \textit{34} & QDP & 4.5 v 5 & Eq. Area & Cr-10 & \cellcolor[HTML]{C4DAF1}2.07 & \cellcolor[HTML]{C4DAF1}1.47 & \colorbox[HTML]{C4DAF1}{2.68}\\
        \textit{35} & QDP & 4.5 v 5 & Eq. Height & PDF & \cellcolor[HTML]{EDF3FB}0.78 & \cellcolor[HTML]{EDF3FB}0.15 & \colorbox[HTML]{EDF3FB}{1.40}\\
        \textit{36} & QDP & 4.5 v 5 & Eq. Height & Cr-20 & \cellcolor[HTML]{DBE7F6}1.69 & \cellcolor[HTML]{DBE7F6}1.09 & \colorbox[HTML]{DBE7F6}{2.31}\\
        \textit{37} & QDP & 4.5 v 5 & Eq. Height & Cr-10 & \cellcolor[HTML]{DBE7F6}1.39 & \cellcolor[HTML]{DBE7F6}0.78 & \colorbox[HTML]{DBE7F6}{2.00}\\
        \bottomrule
    \end{tabular}
    }
    }
\label{tab:model1}
\vspace{-5mm}
\end{table}


% \subsubsection{Visual Analysis of Posteriors}
% \label{sec:visual-results}
% In the above subsection, we investigated all of our pre-registered hypotheses and walked through a breakdown of the numeric outputs associated with our model's posteriors to determine if meaningful differences in performance exist. In this section, we walk through a visual analysis of the posteriors, pointing out major patterns that we observe. For every pattern we discuss, we refer back to Table~\ref{tab:model1} to include information on the existence, or lack thereof, of meaningful differences.

% The first major pattern that we recognize in Figure~\ref{fig:posteriors} is that QDPs appear to be very robust to equal height scaling; the top (equal area) and bottom (equal height) purple QDP posteriors have similar curve shapes and x-axis placements within each SD Pair condition. We also notice this pattern is not recognizable across the other visualizations' posteriors. In Section~\ref{sec:hyp-results} we discovered that PDFs show a meaningful decrease in performance when scaled from equal areas to equal heights. Rows 2 and 3 in Table~\ref{tab:model1} demonstrate that Croissant-10s and -20s also result in a meaningful decrease when equally scaled, whereas QDPs do not exhibit such a decrease (row 4).

% Secondly, we observe QDPs performing to the extremes for each SD Pair. For most SD Pairs QDPs result in the highest accuracy of all tested visualizations, and when used to compare cumulative probabilities of distributions with 4.5 and 5 SDs, QDPs result in the lowest, nearly zero likelihood of task correctness. While this patten is visually obvious, we can confirm that performance across SD Pairs is meaningfully different for QDPs 4.5 v 5 and all other SD Pairs by examining the effects in rows 29-31 of Table~\ref{tab:model1}. This finding is conducive with our affordance-based reasoning about QDPs in Section~\ref{sec:aff-analysis}, and we discuss it further, along with other correlations between affordance and performance, in Section~\ref{sec:task-aff-correlation}.

% Lastly, we observe that although Croissant-20s and -10s do not increase task performance to the extent that QDPs do in most SD Pair conditions, croissant charts consistently visually outperfom PDFs, especially in the equal height condition. In Section~\ref{sec:hyp-results} we confirm that this improvement over PDF performance is meaningful for equal height Croissant-20s across all SD Pairs, and meaningful for equal height Croissant-10s across two of the four SD Pair conditions. %Although other performance improvements may not be statistically meaningful, they are consistently visually apparent.

\subsection{Affordances Described in Open-Ended Responses}
\label{sec:aff-results}
Two raters qualitatively coded strategies from participants' open-ended responses. The raters also identified responses likely AI-generated when they referenced elements not present in the stimuli (e.g., labels, y-axes). Of the 808 responses, \revi{21 were identified by both and excluded from coding. We include the codes of all other responses for a more conservative analysis. All qualitative coding data and analyses are available in the Supplemental Materials.}

The \revi{review of open-ended responses} identified six strategies (mean ICC = 0.84, SD = 0.08): counting, height comparison, area comparison, spread comparison, judgment of how far into a visual mark a threshold occurred (i.e., ``inter-edge interpolation'', Fig.~\ref{fig:cut-off-dist}), and comparison of only marks directly above the threshold (i.e., ``directly over tick''). We show the percentage of participants who mentioned each strategy by \textit{Visualization} condition in Figure~\ref{fig:aff-counts}.

The results indicate that \qdp{QDPs} afforded counting (68\% of participants) more than any other visualization. This 
affordance aligns with initial pilot data and \qdp{QDPs}' frequency-framing motivation~\cite{kay-qdps}. \cten{Croissant-10s}~(23\%) and \ctw{-20s}~(33\%) resulted in roughly \revi{one-third to one-fourth} the number of counting strategies as \qdp{QDPs}, indicating a present, but weaker affordance. \ctw{C}\cten{r}\ctw{o}\cten{i}\ctw{s}\cten{s}\ctw{a}\cten{n}\ctw{t} \cten{c}\ctw{h}\cten{a}\ctw{r}\cten{t}\ctw{s}' counting affordance was exhibited in responses, such as ``... I looked at the number of 5\% `blocks' [that] were on one side on both charts.'' % and ``I looked for the one that had the smallest amount to the right on the number mentioned and them [sic] chose the other as having a higher probablility[sic].'' 
We did not observe any evidence that \pdf{PDFs} afforded counting.
 Figure~\ref{fig:aff-counts} also shows that there was very little evidence that \qdp{QDPs} afforded multiple strategies, in contrast to the other three visualizations.
%Our qualitative analysis highlights the strong affordance of QDPs for counting strategies, reinforcing their intended frequency-framing motivation. Additionally, QDPs showed minimal evidence of alternative strategies, whereas croissant charts supported a more diverse range of approaches, including height and area comparisons, distribution width assessments, and threshold-based judgments. 
This pattern indicates that \ctw{c}\cten{r}\ctw{o}\cten{i}\ctw{s}\cten{s}\ctw{a}\cten{n}\ctw{t} \cten{c}\ctw{h}\cten{a}\ctw{r}\cten{t}\ctw{s} and \pdf{PDFs} result in greater flexibility in strategy use than \qdp{QDPs}.%In the following subsection, we discuss the relationship between our affordance and task performance findings.


\begin{figure}[b!]
\centering  
\vspace{-2mm}
\includegraphics[width=0.9\linewidth, alt={An annotated heat map shows the percent of participants that saw each of the visualization conditions (QDP, PDF, Croissant-20, and Croissant-10) and reported using different strategies when comparing distributions (counting, comparing height, area, spread, inter-edge interpolation, and whether the visual objects were directly over a a tick mark). QDPs show a high concentration (68\%) of participants reporting a counting strategy, whereas PDFs show no counting strategies, and both croissants led to ~20 to 30\% of participants reporting counting.  Additionally, 10\% of  croissant-10 participants reported using inter-edge interpolation, whereas only 0 to 1\% of other conditions' participants reported the same. PDFs and both croissants show a range of strategies reported, whereas QDPs show only one strategy (counting) reported by 68\% of participants and other strategies reported by between 1 and 4\% of participants. The last column (1 to 4\%) shows percentage of participant responses we believe to be AI-written, across visualization condition.}]{figs/qual-heatmap-yb.pdf}
\vspace{-2mm}
    \caption{Percent of each visualization that led to each strategy (columns) across tested visualizations (rows). %Codes are averaged from counts by two qualitative reviewers and normalized by sample size. 
    \rev{Strategies are not mutually exclusive so rows and columns may not equal 100\%.}}
    \label{fig:aff-counts}
    \vspace{-5mm}
\end{figure}

\subsection{Task Performance and Observed Affordances}
\label{sec:task-aff-correlation}
The results in Figure~\ref{fig:aff-counts} show that \qdp{QDPs} strongly afforded counting strategies, 
\ctw{Croissant-20s} and \cten{-10s} weakly afforded counting, and \pdf{PDFs} did not afford counting at all. When looking at the posteriors of Equation~\ref{eq:model1} in Figure~\ref{fig:posteriors}, we can see that the difference in the strength of visualizations' counting affordances corresponds with their likelihood of leading to correct cumulative probability comparisons between three of the four equal-height conditions we tested. These conditions are 2 vs. 5, 3 vs. 5, and 4 vs. 5 SD pairs, and their relative performance is remarkably consistent across equal-height conditions, which indicates that affording counting strategies could improve cumulative comparisons. %We can even see that Croissant-20s, which have a slightly stronger affordance of counting than Croissant-10s, lead to slight increases in the likelihood of correct comparisons. These correlating patterns in our experimental results present evidence that visualization affordances may be associated with correct task completion.  

Additionally, our quantitative results show that \qdp{QDPs} lead to the lowest likelihood of correct comparisons of distributions with SDs of 4.5 and 5. At the same time, our results exhibit that \qdp{QDPs} lack diversity in their afforded \revi{mental actions}. \pdf{PDFs}, \ctw{Croissant-20s} and \cten{-10s}, on the other hand, afford a variety of strategies. For the 4.5 vs. 5 SD Pair condition, our experimental findings illustrate that visualizations that afford noncounting strategies lead to a higher chance of correct comparisons.

Lastly, equal-height \pdf{PDFs} perform meaningfully worse than equal-area \pdf{PDFs} across all SD Pair conditions, and \pdf{PDFs}' most popular strategy is height comparison. To reason about this decrease, we can refer to the difference in height comparisons' efficacy across equal-area and equal-height \pdf{PDFs}.
Although comparing the peak height of two equal-area \pdf{PDFs} leads to consistently correct judgments of our tested task, peak height comparison between equal-height \pdf{PDFs} does not (Fig.~\ref{fig:pdf-aff}, row a).

\section{Discussion and Limitations}
\label{sec:discussion}
We present an affordance-motivated analysis of PDFs, followed by empirical evidence of the performance and affordances of area-encoded probability distribution visualizations. We do so through a case study of PDFs, which restricts the scope of our findings in the interest of examining the relationship between performance and affordance. Below, we detail the concrete contributions of this work, posit potential extrapolations of our findings, and discuss the limitations of our scoping and methodology, before describing future avenues of affordance research in visualization.

\subsection{Contributions to Affordance Research in Visualizations}
We analyze the relationship between performance and affordance evidence from our study to offer insights about the drivers behind previously documented comparison errors in PDFs \cite{fygenson-padilla-pdf-scaling} and performance improvements from QDPs \cite{kay-qdps, fernandes2018-qdp-cdf, kale2020-qdp}. We found a strong correlation between counting and equal-height visualizations' performance, indicating that counting supports cumulative probability comparisons.
We believe that \qdp{QDPs}' and \ctw{c}\cten{r}\ctw{o}\cten{i}\ctw{s}\cten{s}\ctw{a}\cten{n}\ctw{t} \cten{c}\ctw{h}\cten{a}\ctw{r}\cten{t}\ctw{s}' counting affordance provides indirect evidence of frequency-framing at work; % and the affordance of a part-to-whole relationship.
however, we caution that this conclusion is circumstantial, as participants often struggle to fully articulate their cognitive processes\cite{Nisbett1977-NISTMT}.

Another example of affordance-performance alignment is seen in \cten{Croissant-10s} outperforming \qdp{QDPs} in the 4.5 vs. 5 SD condition, and \cten{Croissant-10s}' stronger affordance of ``inter-edge interpolation.'' This \revi{term} refers to participants counting both the whole units prior to a threshold, and the partial amount of a visual mark that is bisected by a threshold (see Fig.~\ref{fig:cut-off-dist}). Inter-edge interpolation suggests that participants recognize that probability does not change in discrete steps along the boundaries of visual marks, but instead forms a continuous distribution. One of our goals \revi{in designing} croissant charts was to afford inter-edge interpolation, because we hypothesized that \qdp{QDPs} weakly afford this interpolation, which can lead to errors when comparing similar SD pairs.  

We also see that \ctw{Croissant-20s} outperform \qdp{QDPs} in the 4.5 vs. 5 SD condition. This may be because \ctw{Croissant-20s} show higher resolution along the x-axis than the \qdp{QDPs} we tested. Although both charts encode 20 quantiles (i.e., each visual mark equals 5\% probability), \qdp{QDPs} stack quantiles such that moving from one column to the next can jump the cumulative probability by more than one quantile, affording discrete changes that may not exist. When designing \ctw{c}\cten{r}\ctw{o}\cten{i}\ctw{s}\cten{s}\ctw{a}\cten{n}\ctw{t} \cten{c}\ctw{h}\cten{a}\ctw{r}\cten{t}\ctw{s}, we sliced them into vertical quantiles, as opposed to \qdp{QDPs}' vertical and horizontal binning technique. %We did so to better support reader comprehension because horizontal slices of PDFs do not have a strong mathematical interpretation. 
A benefit of this design is afforded continuity and increased detail along the x-axis such that close SD comparisons are more supported. On the other hand, \qdp{QDPs}' binning technique affords counting much more strongly than \ctw{c}\cten{r}\ctw{o}\cten{i}\ctw{s}\cten{s}\ctw{a}\cten{n}\ctw{t}\cten{s}', leading to \qdp{QDPs}' superior performance across less similar SD Pairs. Additionally, increasing \qdp{QDPs}' quantiles would increase their resolution, possibly improving their performance in the 4.5 vs. 5 SD condition.  

% We contribute evidence that rationalizes past PDF and QDP findings and outline a process for examining visualization design. In particular, we describe how researchers can reason about current and ideal visualization affordances, conduct experiments to confirm the existence of affordances, and create purposeful new visualizations.

% 2- relationship between affordances and performances (in context of 1)
%     --> bring in speculative stuff
%     Our preregistered hypothesis anticipated this poor performance, reasoning that comparisons between such similar SDs require either finer-grained counting than 20-quantile QDPs offer or the use of an alternate comparison strategy. Accurate comparison with QDPs in this context necessitates recognizing that they are discrete approximations of a continuous probability function, requiring interpolation. To mitigate the lack of interpolation afforded by QDPs, increasing resolution from 20 to 50 or 100 quantiles could enable more detailed counting and likely improve comparisons of distributions with similar SDs. However, prior work has reported mixed results when increasing the number of quantiles in QDPs \cite{kay-qdps, fernandes2018-qdp-cdf}.
%     --> pull in theory that claims there may be a causal relationship

% 3- use affordance to confirm and understand the mechanisms that likely contribute to the results of previous studies (QDP and PDF past paper) 

% 4- a process for identifing edges cases in which visualizations will fail. difficult in part because it takes a lot time. this is an expident method. 

% 5- this process of how to build visualizations with affordances
% we have convergin evidence for something but we cant make a causal relationship.

\subsection{Limitations and Future Work}
\label{sec:limitations}
We present a case study of probability visualizations that express distribution shape, which is inherently limited in scope. 
Additionally, we only investigate normal \revi{static} distributions because our case study is built on previous findings with normal distributions~\cite{fygenson-padilla-pdf-scaling}, and because non-normal distributions are significantly more difficult %for experts and \revi{members of the general public} 
to interpret~\cite{peterson1964mode}. Future work should examine skewed and multimodal visualizations to increase the usefulness % and ecological validity
of this research. We also restrict our experiment to investigate a single, common task. Investigating other tasks, such as readers' accurate estimation of cumulative probabilities, %extrapolation of the likelihood of events,
and decision-making, would expand understanding of how a single affordance may correlate to a range of tasks.

Additionally, we used open-ended responses to uncover afforded strategies, which restricts our affordance findings to strategies that participants are conscious of and able to report. Research in psychology cautions against soley using participant-reported evidence, because of their lack of correlation to participant decision-making \cite{Nisbett1977-NISTMT}. Still, this open-ended reporting is useful for generating hypotheses and corroborating the confirmatory behavioral findings. 

Lastly, expanding the study of the relationship between affordance and performance to other types of visualization and other kinds of information is warranted. This expansion would not only broaden our understanding of other visualizations and how their designs drive reader conclusions, but can also be used to hypothesize about visual techniques that can be adopted for probability communication. For example, spatial subdivision in pie charts and tree maps was instrumental to our affordance-motivated PDF redesign.

\section{Conclusion}
We present a case study of cognitive affordances and performance in %area-encoded 
probability distribution visualizations and demonstrate a relationship between the two metrics. In turn, our findings suggest that cognitive affordances not only exist in visualizations, but also can inform hypotheses about their task performance. This work contributes to the growing body of affordance work in visualization, and establishes empirical evidence for the utility of affordances in reasoning about visualization performance and \revi{mental actions}.

\section{Acknowledgments}
This work was funded in part by NSF Grant \#2428149.

\bibliographystyle{eg-alpha-doi} 
\bibliography{egbibsample}       


\end{document}
