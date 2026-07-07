% # Window
% -------
elem(w, window, root).
attr(w, child-layout, "relstatic").


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% #General attributes
attr(main(S), class, ("d-flex"; "flex-col";"bg-opacity-25";"w-100";"p-2";"rounded";"m-2")):-elem(main(S),container,_).
attr(main(S), class, ("bg-info")):-elem(main(S),container,_),not _clinguin_unsat.
attr(main(S), class, ("bg-danger")):-elem(main(S),container,_), _clinguin_unsat.
attr(section(S), class, ("d-flex"; "flex-column"; "align-items-center";"rounded";"p-2";"m-2";"bg-light";"shadow";)):-elem(section(S),container,_).
attr(title(T), class, ("h5";"pb-1")):-elem(title(T),label,_).
attr(title(T), order, 1):-elem(title(T),label,_).
attr(content(C), class, ("d-flex"; "flex-column";"w-100";"p-1";"border-top";"border-bottom")):-elem(content(C),container,_).
attr(content(C), order, 2):-elem(content(C),container,_).
attr(footer(C), class, ("d-flex"; "flex-column";"w-100";"p-1")):-elem(footer(C),container,_).
attr(footer(C), order, 3):-elem(content(C),container,_).
attr(footer_elem(C), class, ("d-flex";"flex-row-reverse")):- elem(footer_elem(C),container,_).
attr(footer_item(C), class, ("m-1";"btn-primary")):- elem(footer_item(C),button,_).
attr(footer_item(C), class, ("m-1")):- elem(footer_item(C),textfield,_).
attr(footer_item(C), class, ("m-1";"btn-outline-dark")):- elem(footer_item(C),dropdown_menu,_).

attr(elem_container(C), class, ("d-flex"; "flex-row"; "align-items-left";"justify-content-between")):-elem(elem_container(C),container,_).
attr(elem_title(C), order, 1):-elem(elem_title(C),_,_).
attr(elem_title(C), class, ("pe-5";"fst-italic")):-elem(elem_title(C),_,_).
attr(elem_title(C), height, "28pt"):-elem(elem_title(C),label,_).
attr(elem_val(C), order, 2):-elem(elem_val(C),_,_).
attr(elem_val(C), class, ("btn-outline";"btn-small";"fw-light")):-elem(elem_val(C),_,_).
attr(elem_val(C), class, ("pe-3";"pt-1";"pb-1")):-elem(elem_val(C),label,_).
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% elem(tabs, tabs, w).
% attr(tabs, class, ("nav-fill")).
%     elem(main_explaination_tab, tabs_item, tabs).
%     attr(main_explaination_tab, title, "Explanation").

%         elem(main_explaination, container, main_explaination_tab).
%     elem(left_tab, tabs_item, tabs).
%     attr(left_tab, class, "w-100").
%     attr(left_tab, title, "Basic").
%         elem(left, container, left_tab).


%     attr((main_explaination_tab;left_tab), (active_class;disabled_class), ("h3")).
%     attr((main_explaination_tab;left_tab), active_class, ("bg-info";"bg-opacity-25";"h3")).

elem(cols, container, w).
attr(cols, child_layout, grid).
attr(cols, class, ("justify-content-center";"gap-3")).

elem(left, container, cols).
attr(left, order, 1).
attr(left, class, ("mw-25")).
attr(left, grid_column, 1).

elem(right, container, cols).
attr(right, order, 2).
attr(right, class, ("mw-75";)).
attr(right, grid_column, 2).


% elem(s, container, right).
% attr(s, order, 2).
% % attr(s, title, "Explanation").
% attr(s, class, ("border";"bg-info";"bg-opacity-10")).

%         elem(main_explaination, container, s).
%         attr(main_explaination, class, ("mt-4")).


elem(main(explanation_conf), container, left).
attr(main(explanation_conf), order, 2).
attr(main(explanation_conf), class, ("mt-5")).

    elem(section(queries), container, main(explanation_conf)).
    attr(section(queries), order, 1).

        elem(title(queries), label, section(queries)).
        attr(title(queries), label, "What did you expect?").

        elem(content(queries), container, section(queries)).

            elem(elem_container(query(A)), container, content(queries)):-query(A,V).
                elem(elem_title(query(A)), label, elem_container(query(A))):-query(A,V).
                attr(elem_title(query(A)), label, A):-query(A,V).
                attr(elem_title(query(A)), class, "text-success"):-query(A,1).
                attr(elem_title(query(A)), class, "text-danger"):-query(A,0).
                attr(elem_title(query(A)), class, "font-monospace"):-query(A,V).
                attr(elem_title(query(A)), tooltip, @format("query({},{})",A,V)):-query(A,V).

                elem(elem_val(query(A)), button, elem_container(query(A))):-query(A,V).
                % attr(elem_val(query(A)), label, "remove"):-query(A,V).
                attr(elem_val(query(A)), icon, "fa-trash"):-query(A,V).
                attr(elem_val(query(A)), class, ("text-danger")):-query(A,V).
                when(elem_val(query(A)), click, call, remove_query(A)):-query(A,V).

        elem(footer(queries), container, section(queries)).

            elem(footer_elem(queries), container, footer(queries)).

                elem(footer_item(query(name)),textfield,footer_elem(queries)).
                attr(footer_item(query(name)),order,3).
                attr(footer_item(query(name)),placeholder,"atom").
                when(footer_item(query(name)),input,context,(query_name,_value)).

                elem(footer_item(query(val)),dropdown_menu,footer_elem(queries)).
                attr(footer_item(query(val)),order,2).
                attr(footer_item(query(val)),class,"text-dark").


                    elem(footer_item(query(val,true)),dropdown_menu_item,footer_item(query(val))).
                    attr(footer_item(query(val,true)),label,true).
                    attr(footer_item(query(val,true)),class,"text-success").
                    when(footer_item(query(val,true)),click,context,(query_val,true)).
                    when(footer_item(query(val,true)),click, update,(footer_item(query(val)),selected,true)).
                    when(footer_item(query(val,true)),click, update,(footer_item(query(val)),class,"text-success")).

                    elem(footer_item(query(val,false)),dropdown_menu_item,footer_item(query(val))).
                    attr(footer_item(query(val,false)),class,"text-danger").
                    attr(footer_item(query(val,false)),label,false).
                    when(footer_item(query(val,false)),click,context,(query_val,false)).
                    when(footer_item(query(val,false)),click, update,(footer_item(query(val)),selected,false)).
                    when(footer_item(query(val,false)),click, update,(footer_item(query(val)),class,"text-danger")).

                elem(footer_item(query(btn)),button,footer_elem(queries)).
                attr(footer_item(query(btn)),order,1).
                attr(footer_item(query(btn)),label,"Add query").
                when(footer_item(query(btn)),click,call, add_query(_context_value(query_name,const),_context_value(query_val))).

            elem(footer_elem(nl_queries), container, footer(queries)).

                elem(footer_item(nl_query(name)),textfield,footer_elem(nl_queries)).
                attr(footer_item(nl_query(name)), width, "180pt").
                attr(footer_item(nl_query(name)),order,3).
                attr(footer_item(nl_query(name)), placeholder, "Activate LLM first") :- not llm_active.
                attr(footer_item(nl_query(name)), placeholder, "Enter a question") :- llm_active.
                attr(footer_item(nl_query(name)), class, ("opacity-25";"m-1")) :- not llm_active.
                attr(footer_item(nl_query(name)), class, "m-1") :- llm_active.
                when(footer_item(nl_query(name)),input,context,(nl_query,_value)).

                elem(footer_item(nl_query(btn)),button,footer_elem(nl_queries)).
                attr(footer_item(nl_query(btn)),order,1).
                attr(footer_item(nl_query(btn)),label,"Add NL query").
                attr(footer_item(nl_query(btn)), class, ("btn-primary";"opacity-25")) :- not llm_active.
                attr(footer_item(nl_query(btn)), class, "btn-primary") :- llm_active.
                when(footer_item(nl_query(btn)), click, call, add_nl_query(_context_value(nl_query, str))) :-
                llm_active.
                attr(footer_item(nl_query(btn)), tooltip, "Activate the LLM to use this feature") :- not llm_active.

            elem(footer_elem(clear_queries), container, footer(queries)).
            attr(footer_elem(clear_queries), order, 3).

                elem(footer_item(clear_queries), button, footer_elem(clear_queries)).
                attr(footer_item(clear_queries), label, "Clear").
                attr(footer_item(clear_queries), class, ("btn-danger";"align-self-end")).
                attr(footer_item(clear_queries), icon, "fa-trash").
                when(footer_item(clear_queries), click, call, clear_queries).



    % elem(section(configuration), container, main(explanation_conf)).
    % attr(section(configuration), order, 3).

    %     elem(title(configuration), label, section(configuration)).
    %     attr(title(configuration), label, "Configuration").

    %         elem(content(configuration), container, section(configuration)).

    %         egraph((reference;model(reference);foil;model(foil))).
    %         emodel(model(reference);model(foil)).
    %         refmodel(model(reference);reference).
    %         elem(check(G), checkbox, content(configuration)):-egraph(G).
    %         attr(check(model(G)), label, @concat(G, " model")):-egraph(model(G)), emodel(model(G)).
    %         attr(check(G), label, @concat(G, " program graph ")):-egraph(G), not emodel(G).
    %         attr(check(G), checked, true):-show(G), refmodel(G).
    %         attr(check(G), checked, true):-show(G), not refmodel(G), not _no_foil.
    %         attr(check(model(foil);foil), disabled, true):-_no_foil.
    %         when(check(G), click, call, add_shown_graph(G)):-egraph(G), not show(G).
    %         when(check(G), click, call, remove_shown_graph(G)):-egraph(G), show(G).


    elem(section(exbrowse), container, main(explanation_conf)).
    attr(section(exbrowse), order, 2).

        elem(title(exbrowse), label, section(exbrowse)).
        attr(title(exbrowse), label, "Browsing explanations").

        elem(content(exbrowse), container, section(exbrowse)).



                elem(footer_elem(next_explanation), container, content(exbrowse)).

                    elem(footer_item(next_explanation), button, footer_elem(next_explanation)).
                    attr(footer_item(next_explanation), icon, "fa-forward-step").
                    attr(footer_item(next_explanation), label, "Next Explanation").
                    attr(footer_item(next_explanation), class, "btn-primary").
                    when(footer_item(next_explanation), click, call, next_explanation).

        elem(footer(exbrowse), container, section(exbrowse)).

            elem(footer_elem(exdownload_graph), container, footer(exbrowse)).

                elem(footer_item(download(download_name_exg)),textfield,footer_elem(exdownload_graph)).
                attr(footer_item(download(download_name_exg)),order,1).
                attr(footer_item(download(download_name_exg)),placeholder,"explanation_graph.svg").
                when(footer_item(download(download_name_exg)),input,context,(download_name_exg,_value)).

                elem(footer_item(exdownload_graph(btn)),button,footer_elem(exdownload_graph)).
                attr(footer_item(exdownload_graph(btn)),order,3).
                attr(footer_item(exdownload_graph(btn)),label,"Download graph").
                attr(footer_item(exdownload_graph(btn)),icon,"fa-diagram-project").
                attr(footer_item(exdownload_graph(btn)),class,"btn-success").
                when(footer_item(exdownload_graph(btn)),click,call, download_explanation_graph(_context_value(download_name_exg,str,"explanation_graph"))).

            elem(footer_elem(exdownload), container, footer(exbrowse)).

                elem(footer_item(download(download_name_ex)),textfield,footer_elem(exdownload)).
                attr(footer_item(download(download_name_ex)),order,1).
                attr(footer_item(download(download_name_ex)),placeholder,"explanation_facts.lp").
                when(footer_item(download(download_name_ex)),input,context,(download_name_ex,_value)).

                elem(footer_item(exdownload(btn)),button,footer_elem(exdownload)).
                attr(footer_item(exdownload(btn)),order,3).
                attr(footer_item(exdownload(btn)),label,"Download facts").
                attr(footer_item(exdownload(btn)),icon,"fa-download").
                attr(footer_item(exdownload(btn)),class,"btn-success").
                when(footer_item(exdownload(btn)),click,call, download_explanation_facts(_context_value(download_name_ex,str,"explanation_facts"))).



% elem(main(explanation_llm), container, right).
% attr(main(explanation_llm), order, 2).
% attr(main(explanation_llm), class, ("v-flex";"justify-content-center";"align-items-center";"px-3")).

%     elem(section(explanation_llm), container, main(explanation_llm)).
%     attr(section(explanation_llm), order, 1).
%     attr(section(explanation_llm), class, ("p-4";"gap-4";"w-100")).

%         elem(title(explanation_llm), label, section(explanation_llm)).
%         attr(title(explanation_llm), label, "Natural Language Explanation").

%         elem(content(explanation_llm), container, section(explanation_llm)).
%         attr(content(explanation_llm), class, ("p-4";"border";"align-items-center";"bg-body";"rounded")).

%         elem(button(get_llm_explanation), button, content(explanation_llm)) :- not llm_active.
%         attr(button(get_llm_explanation), order, 1).
%         attr(button(get_llm_explanation), label, "Compute using LLM").
%         attr(button(get_llm_explanation), icon, "fa-forward-step").
%         attr(button(get_llm_explanation), class, "btn-primary").
%         when(button(get_llm_explanation), click, call, get_llm_explanation).


elem(main(explanation_graph), container, right).
attr(main(explanation_graph), order, 4).
attr(main(explanation_graph), class, ("d-flex";"justify-content-center";"align-items-center";"px-3")).

    elem(section(explanation_info), container, main(explanation_graph)).
    attr(section(explanation_info), order, 3).
    attr(section(explanation_info), class, ("d-flex";"justify-content-center";"align-items-center";"w-100")).


        elem(info_container, container, section(explanation_info)).
        attr(info_container, order, 2).
        attr(info_container, height, 30).
        attr(info_container, class, ("mb-3")).

            % elem(info_container(X), container, main_explaination):-vnode(X).
            % attr(info_container(X), class, "border"):-vnode(X).

                elem(rule(X), label, info_container):-vnode(X).
                attr(rule(X), order, 1):-vnode(X).
                attr(rule(X), class, ("font-monospace";"fw-light";"text-center")):-vnode(X).
                attr(rule(X), label, L):-vnode(X), tag(X,rule_fo(L)).
                attr(rule(X), label, ""):-vnode(X), not tag(X,rule_fo(_)).
                attr(rule(X), display, none):-vnode(X).

                elem(label(X), label, info_container):-vnode(X).
                attr(label(X), order, 2):-vnode(X).
                attr(label(X), class, ("fst-italic";"text-center")):-vnode(X).
                attr(label(X), label,  @format(L,P)):-vnode(X), tag(X,label(L,P)).
                attr(label(X), label, ""):-vnode(X), not tag(X,label(_,_)).
                attr(label(X), display, none):-vnode(X).


        elem(text(explanation_llm), label, section(explanation_info)).
        attr(text(explanation_llm), order, 2).
        attr(text(explanation_llm), class, ("pt-2";"pb-2";"fst-italic";"text-primary")).
        attr(text(explanation_llm), label, TXT) :- llm_explanation(TXT).


    elem(graph_container, container, main(explanation_graph)).
    attr(graph_container, order, 3).
    attr(graph_container, class, ("d-flex";"justify-content-center";"align-items-center";"p-2";)).
    attr(graph_container, width, "100%").
    attr(graph_container, "overflow-y", scroll).
    attr(graph_container, "overflow-x", scroll).

        %%%%%%%%%%%%%%%%%%%%%%%%
        % Clingraph image
        %%%%%%%%%%%%%%%%%%%%%%%%

        vnode(X):-node(X,_).
        vtag(X,T):-tag(X, T).

        elem(c, canvas, graph_container).
        attr(c, order, 2).
        % attr(c, "transform-origin", "top left").
        % attr(c, display, "inline-block").
        attr(c, width, 600).
        attr(c, height, 550).
        attr(c, transform, "scale(0.8)").
        % attr(c, "transform-origin", "0 0").

        attr(c, image_type, clingraph).
            elem(n(X), svg_node, c) :- vnode(X).
            attr(n(X), clingraph_id, X) :- vnode(X).
            when(n(X), mouseenter, update, ((rule(X);label(X)),display,block)):- vnode(X).
            when(n(X), mouseleave, update, ((rule(X);label(X)),display,none)):- vnode(X).

% elem(main(state), container, left).
% attr(main(state), order, 1).

    % % ## Files
    % % ------------

    % elem(section(files), container, main(state)).

    %     elem(title(files), label, section(files)).
    %     attr(title(files), label, "Files").

    %     elem(content(files), container, section(files)).


    % % ## Constants
    % % ------------

    % elem(section(constants), container, main(state)).

    %     elem(title(constants), label, section(constants)).
    %     attr(title(constants), label, "Constants").

    %     elem(content(constants), container, section(constants)).

    %         elem(elem_container(const(C)), container, content(constants)):-_clinguin_const(C,V).

    %             elem(elem_title(const(C)), label, elem_container(const(C))):-_clinguin_const(C,V).
    %             attr(elem_title(const(C)), label, @format("#const {}",C)):-_clinguin_const(C,V).

    %             elem(elem_val(const(C)), label, elem_container(const(C))):-_clinguin_const(C,V).
    %             attr(elem_val(const(C)), label,V):-_clinguin_const(C,V).
    %             % attr(const_label(C), class, "w-100"):-_clinguin_const(C,V).

    %     elem(footer(constants), container, section(constants)).

    %         elem(footer_elem(constants), container, footer(constants)).

    %             elem(footer_item(const(name)),textfield,footer_elem(constants)).
    %             attr(footer_item(const(name)),placeholder,"name").
    %             attr(footer_item(const(name)),width,"60pt").
    %             when(footer_item(const(name)),input,context,(const_name,_value)).

    %             elem(footer_item(const(val)),textfield,footer_elem(constants)).
    %             attr(footer_item(const(val)),placeholder,"value").
    %             attr(footer_item(const(val)),width,"60pt").
    %             when(footer_item(const(val)),input,context,(const_value,_value)).

    %             elem(footer_item(const(btn)),button,footer_elem(constants)).
    %             attr(footer_item(const(btn)),label,"Set constant").
    %             when(footer_item(const(btn)),click,call, set_constant(_context_value(const_name),_context_value(const_value))).


    % #Todo how do we pass the opt properly?


    % % ## Optimization
    % % -------------
    % elem(section(opt), container, main(state)).

    %     elem(title(opt), label, section(opt)).
    %     attr(title(opt), label, "Optimization").


    %     elem(content(opt), container, section(opt)).
    %     elem(elem_container(opt(cost)), container, content(opt)).
    %     elem(elem_container(opt(optimizing)), container, content(opt)).
    %     elem(elem_container(opt(optimal)), container, content(opt)).

    %         elem(elem_title(opt(cost)), label, elem_container(opt(cost))).
    %         attr(elem_title(opt(cost)), label, "Cost").

    %         elem(elem_val(opt(cost)), label, elem_container(opt(cost))).
    %         attr(elem_val(opt(cost)), icon, "fa-circle-check").
    %         attr(elem_val(opt(cost)), label, Cost):-_clinguin_cost(Cost).



    %         elem(elem_title(opt(optimal)), label, elem_container(opt(optimal))).
    %         attr(elem_title(opt(optimal)), label, "Optimal").

    %         elem(elem_val(opt(optimal)), button, elem_container(opt(optimal))).
    %         attr(elem_val(opt(optimal)), icon, "fa-circle-check").
    %         attr(elem_val(opt(optimal)), class, ("disabled";"border-0";"opacity-100")).
    %         attr(elem_val(opt(optimal)), icon, "fa-circle-check"):-_clinguin_optimal.
    %         attr(elem_val(opt(optimal)), class, ("text-success")):-_clinguin_optimal.
    %         attr(elem_val(opt(optimal)), icon, "fa-circle-xmark"):-not _clinguin_optimal.
    %         attr(elem_val(opt(optimal)), class, ("text-danger")):-not _clinguin_optimal.

    %         elem(elem_title(opt(optimizing)), label, elem_container(opt(optimizing))).
    %         attr(elem_title(opt(optimizing)), label, "Optimizing").

    %         elem(elem_val(opt(optimizing)), button, elem_container(opt(optimizing))).
    %         attr(elem_val(opt(optimizing)), class, ("disabled";"border-0";"opacity-100")).
    %         attr(elem_val(opt(optimizing)), icon, "fa-circle-check"):-_clinguin_optimizing.
    %         attr(elem_val(opt(optimizing)), class, ("text-success")):-_clinguin_optimizing.
    %         attr(elem_val(opt(optimizing)), icon, "fa-circle-xmark"):-not _clinguin_optimizing.
    %         attr(elem_val(opt(optimizing)), class, ("text-danger")):-not _clinguin_optimizing.



% elem(main(input), container, left).
% attr(main(input), order, 2).


    % %  ## Input Atoms
    % %  ---------------
    % elem(section(atoms), container, main(input)).

    %     elem(title(atoms), label, section(atoms)).
    %     attr(title(atoms), label, "Added atoms").

    %     elem(content(atoms), container, section(atoms)).

    %         elem(elem_container(atom(A)), container, content(atoms)):-_clinguin_atom(A).

    %             elem(elem_title(atom(A)), label, elem_container(atom(A))):-_clinguin_atom(A).
    %             attr(elem_title(atom(A)), label, A):-_clinguin_atom(A).
    %             attr(elem_title(atom(A)), class, "font-monospace"):-_clinguin_atom(A).

    %             elem(elem_val(atom(A)), button, elem_container(atom(A))):-_clinguin_atom(A).
    %             % attr(elem_val(atom(A)), label, "remove"):-_clinguin_atom(A).
    %             attr(elem_val(atom(A)), icon, "fa-trash"):-_clinguin_atom(A).
    %             attr(elem_val(atom(A)), class, ("text-danger")):-_clinguin_atom(A).
    %             when(elem_val(atom(A)), click, call, remove_atom(A)):-_clinguin_atom(A).

    %     elem(footer(atoms), container, section(atoms)).

    %         elem(footer_elem(atoms), container, footer(atoms)).

    %             elem(footer_item(atom(name)),textfield,footer_elem(atoms)).
    %             attr(footer_item(atom(name)),placeholder,"atom").
    %             attr(footer_item(atom(name)),class,("align-middle")).
    %             when(footer_item(atom(name)),input,context,(atom_name,_value)).

    %             elem(footer_item(atom(btn)),button,footer_elem(atoms)).
    %             attr(footer_item(atom(btn)),label,"Add atom").
    %             when(footer_item(atom(btn)),click,call, add_atom(_context_value(atom_name))).

    %         elem(footer_elem(clear_atoms), container, footer(atoms)).

    %         elem(footer_item(clear_atoms), button, footer(atoms)).
    %         attr(footer_item(clear_atoms), label, "Clear").
    %         attr(footer_item(clear_atoms), class, "btn-danger").
    %         attr(footer_item(clear_atoms), icon, "fa-trash").
    %         when(footer_item(clear_atoms), click, call, clear_atoms).


    % %  ## Input Externals
    % %  ---------------
    % elem(section(externals), container, main(input)).

    %     elem(title(externals), label, section(externals)).
    %     attr(title(externals), label, "Externals").

    %     elem(content(externals), container, section(externals)).

    %         elem(elem_container(external(A)), container, content(externals)):-_clinguin_external(A,V).

    %             elem(elem_title(external(A)), label, elem_container(external(A))):-_clinguin_external(A,V).
    %             attr(elem_title(external(A)), label, A):-_clinguin_external(A,V).
    %             % attr(elem_title(external(A)), class, "text-success"):-_clinguin_external(A,true).
    %             % attr(elem_title(external(A)), class, "text-danger"):-_clinguin_external(A,false).
    %             attr(elem_title(external(A)), class, "font-monospace"):-_clinguin_external(A,V).

    %             elem(elem_val(external(A)), dropdown_menu, elem_container(external(A))):-_clinguin_external(A,V).
    %             attr(elem_val(external(A)), selected, V):-_clinguin_external(A,V).
    %             attr(elem_val(external(A)), class, "text-success"):-_clinguin_external(A,true).
    %             attr(elem_val(external(A)), class, "text-danger"):-_clinguin_external(A,false).


    %                 elem(elem_val(external(A),true), dropdown_menu_item, elem_val(external(A))):-_clinguin_external(A,V).
    %                 attr(elem_val(external(A),true), label, "true"):-_clinguin_external(A,V).
    %                 attr(elem_val(external(A),true), class, "text-success"):-_clinguin_external(A,V).
    %                 when(elem_val(external(A),true), click, call, set_external(A,true)):-_clinguin_external(A,V).

    %                 elem(elem_val(external(A),false), dropdown_menu_item, elem_val(external(A))):-_clinguin_external(A,V).
    %                 attr(elem_val(external(A),false), label, "false"):-_clinguin_external(A,V).
    %                 attr(elem_val(external(A),false), class, "text-danger"):-_clinguin_external(A,V).
    %                 when(elem_val(external(A),false), click, call, set_external(A,false)):-_clinguin_external(A,V).

    %                 elem(elem_val(external(A),release), dropdown_menu_item, elem_val(external(A))):-_clinguin_external(A,V).
    %                 attr(elem_val(external(A),release), label, "release"):-_clinguin_external(A,V).
    %                 when(elem_val(external(A),release), click, call, set_external(A,release)):-_clinguin_external(A,V).


elem(main(model), container, left).
attr(main(model), order, 1).

    %  ## Model
    %  ---------------

    %  ## Model
    %  ---------------

    elem(section(model), container, main(model)).
    attr(section(model), order, 1).

    elem(content(model), container, section(model)).
    attr(content(model), class, ("d-flex";"flex-row")).

            elem(title(model), label, section(model)).
            attr(title(model), label, "Reference model").

            _any_or_browse(A):-_clinguin_browsing, _clinguin_model(A).
            _any_or_browse(A):-not _clinguin_browsing, _any(A).

            show_model(X):-_any_or_browse(X).
            show_model(X):-_clinguin_assume(X,_).


            elem(sub_content(model), container, content(model)).



                elem(elem_container(model(A)), container, sub_content(model)):-show_model(A).

                    elem(elem_title(model(A)), button, elem_container(model(A))):-show_model(A).
                    % attr(elem_title(model(A)), label, A):-show_model(A).
                    attr(elem_title(model(A)), label, A):-show_model(A).
                    attr(elem_title(model(A)), class, "font-monospace"):-show_model(A).
                    attr(elem_title(model(A)), class, "text-decoration-underline"):-  show_model(A),  _clinguin_assume(A,true).
                    attr(elem_container(model(A)), tooltip, @concat(A, " is included by the user from the model")):-  show_model(A),  _clinguin_assume(A,true).
                    attr(elem_title(model(A)), class, ("text-decoration-line-through")):-  show_model(A),  _clinguin_assume(A,false).
                    attr(elem_container(model(A)), tooltip, @concat(A, " is excluded by the user from the model")):-  show_model(A),  _clinguin_assume(A,false).
                    % attr(elem_title(model(A)), opacity, "0.4"):-  show_model(A), not _clinguin_model(A).
                    attr(elem_title(model(A)), class, "fw-bold"):-  show_model(A), _all(A).
                    attr(elem_container(model(A)), tooltip, @concat(A, " is in all models")):-  show_model(A), _all(A).
                    attr(elem_title(model(A)), class, "opacity-25"):-  _any(A), not _clinguin_model(A).
                    attr(elem_container(model(A)), tooltip, @concat(A, " is some model but not in the current one")):-  _any(A), not _clinguin_model(A).

                    when(elem_title(model(A)), click, update, (elem_cm(model(A)), visibility, shown)):-  show_model(A).


                    elem(elem_cm(model(A)), context_menu,w):-show_model(A).

                        elem(elem_cm(model(A),force), button,elem_cm(model(A))):-show_model(A).
                        attr(elem_cm(model(A),force), label,"Force in model"):-show_model(A).
                        when(elem_cm(model(A),force), click, call, add_assumption(A,true)):-show_model(A),not _clinguin_assume(A,_), _any(A).
                        attr(elem_cm(model(A),force), class, ("disabled";"text-light")):-show_model(A),not when(elem_cm(model(A),force),_,_,_).

                        elem(elem_cm(model(A),remove), button,elem_cm(model(A))):-show_model(A).
                        attr(elem_cm(model(A),remove), label,"Remove from model"):-show_model(A).
                        when(elem_cm(model(A),remove), click, call, add_assumption(A,false)):-show_model(A),not _clinguin_assume(A,_), not _all(A).
                        attr(elem_cm(model(A),remove), class, ("disabled";"text-light")):-show_model(A),not when(elem_cm(model(A),remove),_,_,_).

                        elem(elem_cm(model(A),clear), button,elem_cm(model(A))):-show_model(A).
                        attr(elem_cm(model(A),clear), label,"Clear selection"):-show_model(A).
                        when(elem_cm(model(A),clear), click, call, remove_assumption(A)):-show_model(A),_clinguin_assume(A,_).
                        attr(elem_cm(model(A),clear), class, ("disabled";"text-light")):-show_model(A),not when(elem_cm(model(A),clear),_,_,_).


            elem(footer(model), container, section(model)).



            % elem(footer_elem(select), container, footer(model)).
            % attr(footer_elem(select), order, 2).

            %     elem(footer_item(select(select_show)),textfield,footer_elem(select)).
            %     attr(footer_item(select(select_show)),order,1).
            %     attr(footer_item(select(select_show)),width,"315pt").
            %     attr(footer_item(select(select_show)),placeholder,"Optional #show").
            %     when(footer_item(select(select_show)),input,context,(select_show,_value)).

            %     elem(footer_item(select(btn)),button,footer_elem(select)).
            %     attr(footer_item(select(btn)),order,2).
            %     attr(footer_item(select(btn)),label,"Select").
            %     attr(footer_item(select(btn)),icon,"fa-hand-pointer").
            %     attr(footer_item(select(btn)),class,"btn-success").
            %     when(footer_item(select(btn)),click,call, select(_context_value(select_show,str," "))).


            % elem(footer_elem(download), container, footer(model)).
            % attr(footer_elem(download), order, 3).

            %     elem(footer_item(download(download_show)),textfield,footer_elem(download)).
            %     attr(footer_item(download(download_show)),order,2).
            %     attr(footer_item(download(download_show)),placeholder,"Optional #show").
            %     when(footer_item(download(download_show)),input,context,(download_show,_value)).

            %     elem(footer_item(download(download_name)),textfield,footer_elem(download)).
            %     attr(footer_item(download(download_name)),order,1).
            %     attr(footer_item(download(download_name)),placeholder,"File name").
            %     when(footer_item(download(download_name)),input,context,(download_name,_value)).

            %     elem(footer_item(download(btn)),button,footer_elem(download)).
            %     attr(footer_item(download(btn)),order,3).
            %     attr(footer_item(download(btn)),label,"Download").
            %     attr(footer_item(download(btn)),icon,"fa-download").
            %     attr(footer_item(download(btn)),class,"btn-success").
            %     when(footer_item(download(btn)),click,call, download(_context_value(download_show,str," "),_context_value(download_name,str,"file.lp"))).


            elem(footer_elem(browse), container, footer(model)).
            attr(footer_elem(browse), order, 1).

                elem(footer_item(next_solution), button, footer_elem(browse)).
                attr(footer_item(next_solution), order, 3).
                attr(footer_item(next_solution), label, "Next").
                attr(footer_item(next_solution), icon, "fa-forward-step").
                when(footer_item(next_solution), click, call, next_solution).

                % elem(footer_item(next_solution_opt), button, footer_elem(browse)).
                % attr(footer_item(next_solution_opt), order, 2).
                % attr(footer_item(next_solution_opt), label, "Next Optimizing").
                % attr(footer_item(next_solution_opt), icon, "fa-forward-fast").
                % when(footer_item(next_solution_opt), click, call, next_solution(optN)).

                elem(footer_item(stop), button, footer_elem(browse)).
                attr(footer_item(stop), order, 1).
                attr(footer_item(stop), label, "Stop Browsing").
                attr(footer_item(stop), class, "btn-danger").
                attr(footer_item(stop), class, "disabled"):-not _clinguin_browsing.
                attr(footer_item(stop), icon, "fa-stop").
                when(footer_item(stop), click, call, stop_browsing).
% # Menu bar
% -----------
    elem(menu_bar, menu_bar, w).
    attr(menu_bar, title, "ASPlain").
    attr(menu_bar, icon, "fa-comments").

        elem(menu_bar_restart, button, menu_bar).
        attr(menu_bar_restart, label, "Restart").
        attr(menu_bar_restart, icon, "fa-arrows-rotate").
        attr(menu_bar_restart, class, "btn-outline-danger").
        attr(menu_bar_restart, class, "border-0").
        when(menu_bar_restart, click, call, restart).

        elem(menu_bar_llm, button, menu_bar).
        attr(menu_bar_llm, label, "Activate LLM") :- not llm_active.
        attr(menu_bar_llm, label, "De-activate LLM") :- llm_active.
        attr(menu_bar_llm, icon, "fa-comment-dots").
        attr(menu_bar_llm, class, ("btn-primary";"opacity-25")):- not llm_active.
        attr(menu_bar_llm, class, "btn-primary"):- llm_active.
        when(menu_bar_llm, click, call, activate_llm(true)) :- not llm_active.
        when(menu_bar_llm, click, call, activate_llm(false)) :- llm_active.
